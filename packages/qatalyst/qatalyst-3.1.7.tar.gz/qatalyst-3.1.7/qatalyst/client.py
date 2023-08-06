#
#    (C) Quantum Computing Inc., 2020.
#
#    THIS IS UNPUBLISHED PROPRIETARY SOURCE CODE of the Copyright Holder. 
#    The contents of this file may not be disclosed to third parties, copied 
#    or duplicated in any form, in whole or in part, without the prior written
#    permission of the Copyright Holder.
#
from typing import Tuple, Callable, Union, Any, Optional
import requests
import time
import math
import os
import signal
import sys
from datetime import datetime as dt
from datetime import timezone as tz
import yaml
import json
import numpy as np
import scipy.sparse as sp
import networkx as nx
from warnings import warn
from requests_toolbelt.multipart import encoder

from qatalyst.package_info import __version__

from .encoders import encode_data, encode_sparse_array, encode_ndarray, encode_graph
from .decoders import decodeResponse
from .utils import print_available_samplers, \
    load_available_samplers, \
    get_scipy_minimize_methods, \
    param_check, \
    check_dwave_size, \
    parse_status
from .data_processing import TicToc, Status, StatusCodes, AwsDeviceClient

client_rcvd_timeout_signal = False
def handleAlarmSignal(signum, frame):
    global client_rcvd_timeout_signal

    if signum == signal.SIGALRM:
        print(f'\nReceived Alarm signal {signum} (Timeout)', flush=True)
        client_rcvd_timeout_signal = True
    else:
        print(f'\nReceived signal {signum} in SIGALRM handler (this is a bug).', flush=True)


def registerForAlarmSignals():
    # register the SIGALRM signals to be caught
    signal.signal(signal.SIGALRM, handleAlarmSignal)


def get_client_kwargs(**kwargs):
    """
    From kwargs extract arguments relevant to Client instances.

    :param kwargs: dict, user-provided kwargs
    :return: client arguments dictionary, parameter dictionary
    """
    client_kwargs = {'username': None,
                     'password': None,
                     'access_token': None,
                     'sampler': 'csample',
                     'configuration': 'default',
                     'conf_path': None,
                     'interruptible': False,
                     'url': None}
    for key in client_kwargs:
        if key in kwargs:
            # We use `pop` so that items do not get passed to the
            # server if not necessary.
            client_kwargs[key] = kwargs.pop(key)
    return client_kwargs, kwargs


class HTTPClient:

    # default paths to look for the user configuration file
    CONF_PATHS = ('~/.qci.conf', '~/.qci/qci.conf')

    DEFAULT_API_URL = 'https://api.qci-prod.com'
    API_ENV_VAR = 'QATALYST_API_URL'                # if set in user's environment, overrides DEFAULT_API_URL

    def __init__(self,
                 username: str = None,
                 password: str = None,
                 access_token: str = None,
                 configuration: str = 'default',
                 conf_path: str = None,
                 url: str = None,
                 braket_url: str = None,
                 interruptible: bool = False):
        """Initialize the HTTPClient.

        :param :dict:`options: { url: str, username: str, password: str, access_token: str }`
        """
        self.user_provided_url = False
        if url is not None:
            self.user_provided_url = True
        self.url = url
        self.username = username
        self.password = password
        self.access_token = access_token
        self.interruptible = interruptible
        self.configuration = configuration

        conf = self.get_config(path=conf_path)

        assert configuration in conf, f"Configuration provided, {configuration}, not found in qci.conf file."

        # Select the desired configuration
        self.conf = conf[self.configuration]

        # Using selected config, fill username, password, access_token with conf file
        # values if the former are None
        self.set_attributes()

        # endpoints
        self.post_endpoint = '/queues/submit'
        self.status_endpoint = '/queues/status?JobID={}'
        self.result_endpoint = '/queues/result?JobID={}'

        # braket-specific API variables (braket_url used mostly for testing)
        self.braketcheck_url = braket_url or url
        self.braketcheck_endpoint = '/braketcheck'

        self.JobId = None

        # delay in seconds
        self.delay = 1
        self.delay_incr = 1
        self.max_delay = 10
        self.status_message_written = False
        self.status_codes = StatusCodes

        self._status_time = None
        # self._status = None

        self.proxies = {}
        if os.getenv('HTTP_PROXY') is not None:
            self.proxies['https'] = os.getenv('HTTP_PROXY')
        if os.getenv('HTTPS_PROXY') is not None:
            self.proxies['https'] = os.getenv('HTTPS_PROXY')

        if self.interruptible:
            registerForAlarmSignals()

    @property
    def status_time(self):
        return self._status_time

    @status_time.setter
    def status_time(self, val):
        self._status_time = val

    def __authenticate(self) -> str:
        r"""Try to authenticate against the csample /authorize endpoint"""
        user = {}
        if self.username:
            user['Username'] = self.username

        if self.password:
            user['Password'] = self.password

        if self.access_token:
            user['AccessToken'] = self.access_token

        headers = {"Qatalyst-Version": __version__}

        # this is where QD-222 is having issues
        try:
            if self.proxies:
                print('Using proxy server(s) ', self.proxies, ' to send request')
            res = requests.post(self.url + '/authorize', headers=headers, json=user, proxies=self.proxies)
            if res.status_code == 409:
                raise Exception("Unsupported Qatalyst client, please update the client")
            return res.json()
        except requests.HTTPError as e:
            # TODO: DY, check error
            if self.proxies:
                print('Error using proxy server(s)')
            raise e

    def get_config(self, path=None):
        if path is not None:
            path = os.path.expanduser(path)
            try:
                with open(path, 'r') as fh:
                    conf = yaml.safe_load(fh)
            except FileNotFoundError as e:
                raise e
        else:
            for pth in self.CONF_PATHS:
                # Logic: if the conf file exists and we successfully read it in then
                # we drop through to 'else' and break out of the loop. If 'pth' doesn't exist
                # then continue through path options. If yaml cannot load it, then throw this
                # as a legitimate error.
                try:
                    with open(os.path.expanduser(pth), 'r') as fh:
                        conf = yaml.safe_load(fh)
                # keep looking in CONF_PATHS
                except FileNotFoundError:
                    continue
                except yaml.YAMLError as e:
                    raise e
                else:
                    break
            else:
                locs = ', '.join(['{}'.format(os.path.expanduser(f)) for f in self.CONF_PATHS])
                raise FileNotFoundError('Configuration file not found the following expected locations: {}'.format(locs))
        return conf

    def set_attributes(self):
        """
        Setting attributes in this way is a little awkward looking, but it allows the user to override the values in
        the .qci.conf file by passing in args if desired.
        """
        self.username = self.username if self.username is not None else self.conf.get('username')
        self.password = self.password if self.password is not None else self.conf.get('password')
        self.access_token = self.access_token if self.access_token is not None else self.conf.get('access_token')

        # If an API endpoint url is not specified when a ClientService instance is instantiated (from the user
        #     specifying url='some_server' as a parameter when they created a client using QatalystCore() or QGraphClient,
        # Then we will need to determine an API endpoint for them to use.  Do this using the following sequence:
        # First check to see if the user has set a preferred URL in QCConstants.API_ENV_VAR and use that URL if it exists.
        # Failing that, check to see if qatalyst_api_url is specified in the user's configuration file.
        # As a last resort, set URL to QCConstants.DEFAULT_API_URL
        if not self.user_provided_url:
            api_url_from_env = os.getenv(self.API_ENV_VAR)
            if api_url_from_env:
                self.url = api_url_from_env

            # If url has not been set by any other method, default it here. This ensures that 'url' will have a
            # non-None value if the attempt to set it above failed.
            elif self.conf.get('qatalyst_api_url') is not None:
                self.url = self.conf.get('qatalyst_api_url')
            else:
                self.url = self.DEFAULT_API_URL

    def check_status(self, res: requests.Response) -> Status:
        stat = parse_status(res)
        return stat

    def increment_delay(self):
        """
        Increase the polling delay until we reach 60 seconds between checks. Then check back every 60 seconds.

        :return: None
        """
        if self.delay < self.max_delay:
            self.delay += self.delay_incr
        else:
            self.delay = self.max_delay

    def get_token(self) -> Union[dict, str]:
        if self.username or self.access_token:
            return self.__authenticate()
        else:
            return {'access_token': ''}

    def create_callback(self, enc) -> Callable:
        encoder_len = enc.len
        # get a starting time and return an instance of the TicToc class
        tic = TicToc()

        def callback(monitor, bar_length=20):
            # mean bytes per second and estimated time remaining
            # tic.toc() takes latest time and subtracts start time
            mean_bps = monitor.bytes_read / tic.toc()
            est_remaining = 'Est. remaining (sec): {}'.format(round((encoder_len - monitor.bytes_read) / mean_bps, 1))
            # Calculate fraction of upload to completed and redo the progress bar
            fractional_progress = round(monitor.bytes_read / encoder_len, 2)
            progress = round(100.0 * fractional_progress, 1)
            tick_len = int(round(bar_length * fractional_progress))
            bar = '=' * tick_len + '-' * (bar_length - tick_len)
            # stdout stays on the same line, and \r moves the cursor back to the start
            sys.stdout.write('\rUpload progress [{}] | {}% | {}'.format(bar, progress, est_remaining))
            sys.stdout.flush()

        return callback

    def auth_method(self):
        auth_method = ''
        if self.username:
            auth_method = 'username'
            if self.password:
                auth_method += '+password'
        if self.access_token:
            if auth_method:
                auth_method += '+'
            auth_method += 'access_token'
        return auth_method

    def jobinfo(self):
        jobinfo = {
            'job_id': self.JobId,
            'job_api_endpoint': self.url,
            'job_request_timeout': str(self.request_timeout),
            'job_request_size_bytes': self.job_request_size_bytes,
            'job_request_size_str': self.job_request_size_str,
            'job_started_utc': self.job_started_dt_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),   # elasticsearch strict_date_optional_time_nanos format
            'job_finished_utc': self.job_finished_dt_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),  # elasticsearch strict_date_optional_time_nanos format
            'job_duration': str(self.job_finished_dt_utc - self.job_started_dt_utc),
            'job_auth_method': self.auth_method(),
            'job_connection_errors': str(self.connection_errors),
            'job_reconnects': str(self.reconnects),
            'job_interruptible': str(self.interruptible),
            'job_timeouts': str(self.timeouts)
        }
        return jobinfo

    # TODO: put this somewhere better (like a utilities class)
    @staticmethod
    def nbytes_to_string(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    @staticmethod
    def get_datetime_info():
        now_utc = dt.now(tz.utc)
        now_localtime = dt.fromtimestamp(now_utc.timestamp())
        local_tz = now_utc.astimezone().tzinfo
        local_tz_name = local_tz.tzname(None)
        local_tz_offset = local_tz.utcoffset(None)
        local_tz_offset_hours = local_tz_offset.seconds / (60 * 60)
        if local_tz_offset.days < 0:
            local_tz_offset_hours = local_tz_offset_hours - 24

        datetime_info = {
            'now_utc' : now_utc,
            'now_localtime' : now_localtime,
            'local_tz' : local_tz,
            'local_tz_name' : local_tz_name,
            'local_tz_offset' : local_tz_offset,
            'local_tz_offset_hours' : local_tz_offset_hours
        }

        return datetime_info

    @staticmethod
    def get_datetime_str(include_utc=False):
        dt_info = HTTPClient.get_datetime_info()

        localtime_str = dt_info['now_localtime'].ctime()
        local_tz_name = dt_info['local_tz_name']
        local_tz_offset_hours = dt_info['local_tz_offset_hours']
        dt_str = f'{localtime_str} {local_tz_name} ({local_tz_offset_hours})'

        if include_utc:
            now_utc = dt_info['now_utc']
            utc_str = now_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
            dt_str = f'{dt_str} [{utc_str}]'

        return dt_str

    def post_request(self,
                     data: dict,
                     token: dict,
                     timeout=21600) -> None:
        """
        Post a request to the API endpoint at self.post_endpoint.

        :param data: dict, data package
        :param token: dict, contains {'access_token': access_token}
        :param timeout: int, length of time to wait for a job creation response. In seconds.
        :return: None
        """
        with requests.Session() as session:
            enc = encoder.MultipartEncoder(fields=data)
            callback = self.create_callback(enc)
            monitor = encoder.MultipartEncoderMonitor(enc, callback)
            headers = {'Authorization': 'Bearer ' + token['access_token'], "Content-Type": monitor.content_type, "Qatalyst-Version": __version__}

            self.job_request_size_bytes = enc.len
            self.job_request_size_str = self.nbytes_to_string(self.job_request_size_bytes)

            sys.stdout.write(f'\nSending request to {self.url} ({self.job_request_size_str}).\n')
            resp = session.post(self.url + self.post_endpoint, timeout=timeout, headers=headers, data=monitor)

            resp.raise_for_status()

            if resp.status_code == 409:
                raise requests.HTTPError("Unsupported Qatalyst client, please update the client")

            # Make sure the post confirm that the problem was created (== 201)
            if resp.status_code not in [200, 201]:
                raise requests.HTTPError("Job not successfully created.")

            # Report JobId to the user
            self.JobId = resp.json()['JobID']

            # The job is asynchronous. User can check status using the JobId
            sys.stdout.write(f'\n{self.get_datetime_str(include_utc=True)} | Job started with JobID: {self.JobId}.\n')

    def get_status_api(self, token: dict) -> requests.Response:
        if self.proxies:
            print('Using proxy server(s) ', self.proxies, ' to send requests')
        return requests.get(self.url + self.status_endpoint.format(self.JobId),
                            headers={'Authorization': 'Bearer ' + token['access_token'], "Qatalyst-Version": __version__},
                            proxies=self.proxies)

    def report_status_to_user(self, status) -> None:
        if status.status is StatusCodes.complete:
            print(f'\n{self.get_datetime_str()} | Problem COMPLETE, returning solution.\n')
        elif status.status == StatusCodes.error:
            print(f'\n{self.get_datetime_str()} | Encountered ERROR, check traceback.\n')
        else:
            # new message to write
            if not self.status_message_written:
                sys.stdout.write(f'\n{self.get_datetime_str(include_utc=False)} | Problem started\n')
                self.status_message_written = True
            # an updated timestamp --> new status
            if self.status_time is None or status.timestamp > self.status_time:
                self.status_time = status.timestamp
                #TODO switch back to if status.message for Qatalyst 4.0 release
                if status.message and 'No such file' not in status.message:
                    sys.stdout.write(f'{self.get_datetime_str()} | Update: {status.message}\n')
            print(f"{self.get_datetime_str(include_utc=False)} | Checking again in {self.delay} seconds...", end='\r', flush=True)

    def poll_status(self, token: dict) -> Status:
        """
        Check status of JobId at increasing intervals. Starts at Default is adding 2 seconds after each check, until
        max_delay is reached (default = 60 sec)

        :param token: dict, {'access_token', access_token}
        :return: None
        """
        global client_rcvd_timeout_signal

        status = Status(StatusCodes.processing, message='', timestamp=str(dt.now()))
        while status.status is StatusCodes.processing:
            time.sleep(self.delay)
            if client_rcvd_timeout_signal and self.interruptible:
                raise TimeoutError
            res = self.get_status_api(token)
            res.raise_for_status()
            self.increment_delay()
            status = self.check_status(res)
            self.report_status_to_user(status)
        else:
            return status

    def check_braket_status(self, device_name: str, models: str, token: dict):
        """
        :param device_name: str, name of device for lookup purposes on AWS
        :param models: str, list of models assigned to device name
        :param token: dict, {'access_token', access_token}

        :return: dict
        """
        headers = {'Authorization': 'Bearer ' + token['access_token'], "Qatalyst-Version": __version__}
        data = json.dumps({'device_name': device_name, 'models': ','.join(models)})
        if self.proxies:
            print('Using proxy server(s) ', self.proxies, ' to send requests')
        resp = requests.post(self.braketcheck_url + self.braketcheck_endpoint, headers=headers, data=data, proxies=self.proxies)

        # Try letting requests deal with the dictionary itself. This seems to behave
        # differently depending on which system the API is running on. Flask issue or requests quirk??
        if resp.status_code == 500:
            try:
                data = {'device_name': device_name, 'models': ','.join(models)}
                if self.proxies:
                    print('Using proxy server(s) ', self.proxies, ' to send requests')
                resp = requests.post(self.braketcheck_url + self.braketcheck_endpoint, headers=headers, data=data, proxies=self.proxies)
            except Exception as e:
                raise e

        # Carefully handle response object.
        try:
            resp = json.loads(resp.json())
        except json.JSONDecodeError:
            resp = resp.json()
        # something that's not a decoding error
        except (ValueError, TypeError) as e:
            print(f"Content of response: {resp.content}.")
            raise e
        return resp

    def sendRequest(self, data, large_data=False, timeout=21600) -> Any:
        """
        Send a request to the web service
        :param data: dict, contains 'metadata', 'params', and 'data'
        :param large_data: bool, toggle info message if the data is large.
        :param timeout: int, seconds to wait until giving up on posting to the API # TODO: do we still need this?
        :return: JSON response from server
        """
        global client_rcvd_timeout_signal
        if large_data:
            print("Data may take a moment to transfer to the server... ")
        token = self.get_token()
        self.post_request(data, token, timeout)
        self.job_started_dt_utc = dt.now(tz.utc)
        self.reconnects = 0
        self.connection_errors = 0
        self.timeouts = 0
        self.request_timeout = timeout
        trying = True
        threw_exception = False
        status = None
        client_rcvd_timeout_signal = False

        while trying:        # handle possible connection loss
            try:            
                status = self.poll_status(token)
                trying = False
                if threw_exception:
                    self.reconnects += 1
                    print(f"{self.get_datetime_str(include_utc=False)} | Reconnected Successsfully!                               ", end='\r', flush=True)
                    threw_exception = False
            except TimeoutError:
                if self.interruptible:
                    self.timeouts += 1
                    print(f"\n{self.get_datetime_str(include_utc=False)} | Timeout error                                            ", end='\n', flush=True)
                    break
            except:
                print(f"{self.get_datetime_str(include_utc=False)} | Possible connection error                                ", end='\r', flush=True)
                threw_exception = True
                self.connection_errors += 1
                time.sleep(2)
        # complete, error = self.poll_status(token)
        if not status:
            if client_rcvd_timeout_signal and self.interruptible:
                raise TimeoutError("received SIGALRM")  # probably sent from a test framework because current job took too long to complete.
            else:
                raise RuntimeError("Unknown runtime error (status is empty)")
        elif status.status is StatusCodes.error:
            # go get the final status so we can send it to the user
            raise ValueError("Failed with the following error: {}".format(status.message))
        else:
            # get the completed result, or error if there is one
            self.job_finished_dt_utc = dt.now(tz.utc)
            if self.proxies:
                print('Using proxy server(s) ', self.proxies, ' to send requests')
            res = requests.get(self.url + self.result_endpoint.format(self.JobId),
                               headers={'Authorization': 'Bearer ' + token['access_token'], "Qatalyst-Version": __version__},
                               proxies=self.proxies)

            try:
                assert res.status_code == 200
                response = json.loads(decodeResponse(res.text))
                response['jobinfo'] = self.jobinfo()
                return response
            except AssertionError:
                print("Failed Response: status_code = {}\n".format(res.status_code), file=sys.stderr)


class ClientService(HTTPClient):

    BRAKET_ONLINE = 'ONLINE'
    BRAKET_OFFLINE = 'OFFLINE'

    PROBLEM_TYPES = ['qubo', 'constraint_problem', 'graph', 'lagrange_opt']

    DEFAULT_OPTIMIZER = 'cobyla'
    DEFAULT_ALGORITHM = 'vqe'
    CLASSICAL_SAMPLERS = ['csample']
    DEFAULT_OPTIMIZER_PARAMS = {'maxiter': 5}
    DEFAULT_NUM_SHOTS = 100
    DEFAULT_NUM_READS = 100
    DEFAULT_CIRCUIT_DEPTH = 2
    DEFAULT_LAGRANGE_MAX_DEPTH = 5
    OPTIMIZER_PARAMS = {'cobyla': DEFAULT_OPTIMIZER_PARAMS}
    HYBRID_ALGORITHMS = ['qaoa', 'vqe']

    DATA_OBJ_FNAME = 'data_obj.npz'
    DATA_CON_FNAME = 'data_con.npz'
    METADATA_FNAME = 'metadata.txt'
    PARAMS_NAME = 'params.txt'
    #
    # DEFAULT_API_URL = 'https://api.qci-prod.com'
    # API_ENV_VAR = 'QATALYST_API_URL'                # if set in user's environment, overrides DEFAULT_API_URL

    def __init__(self,
                 username: str = None,
                 password: str = None,
                 access_token: str = None,
                 sampler: str = None,
                 configuration: str = 'default',
                 conf_path: str = None,
                 interruptible: bool = False,
                 url: str = None,
                 braket_url: Optional[str] = None,
                 optimizer: str = None,
                 optimizer_params: dict = None,
                 algorithm: str = None):

        """
        Handles specific data processing for input, as well as communicating with the HTTPClient for authorization and
        sending requests to the API.

        Requires a username and password, or a username and access_token in order to complete authorization

        :param username: str
        :param password: str
        :param access_token: str
        :param sampler: str, which sampler to use. Current list is ['csample'].
        :param configuration: str, configuration name, in case the config file contains multiples
        :param conf_path: str, optional path to local configuration file. By default, HttpClient will check in
            these locations: ('~/.qci.conf', '~/.qci/qci.conf').
        :param interruptible: bool, give up if we hit an exception.  Default = False (keep trying)
        :param url: str, if not None, user specified Portal-API server using url='some_server' in their code.
            if the user did not specify a url parameter, we will set it for them here.
        :param optimizer: str, Classical optimizer to use in a quantum-classical hybrid algorithm.
        :param optimizer_params: dict, parameters to pass to the optimizer.
        :param algorithm: str, hybrid algorithm used for solving a QUBO. One of 'qaoa' or 'vqe'.
        """
        # superclass will set self.url from config file if user has defined qatalyst_api_url in their config file
        super().__init__(username=username, password=password, access_token=access_token, configuration=configuration,
                         conf_path=conf_path, url=url, braket_url=braket_url, interruptible=interruptible)

        self.samplers = load_available_samplers()
        # handle backards compatibility with sampler='csample' for version < 2.0.6
        if sampler == 'csample':
            self.sampler = 'csample'
        # default to Advantage if unspecified
        elif sampler == 'braket_dwave':
            self.sampler = 'braket_dwave_advantage'
        else:
            self.sampler = sampler or self.conf.get('sampler', 'csample')
        self.algorithm = None
        self.optimizer = None
        self.optimizer_params = None

        # Braket-specific attributes
        self._arn = None
        self._device: Optional[AwsDeviceClient] = None

        # Make sure the 'target_name' is in the list of available samplers
        assert self.sampler in set(self.samplers['target_name']), \
            f"Sampler must be one of {set(self.samplers['target_name'].to_list())}."

        # If we have a valid hybrid algorithm and ask for a compatible solver, then set the optimizer and params
        if self.sampler in set(self.samplers[self.samplers['hybrid']]['target_name']):

            if algorithm:
                self.algorithm = algorithm.lower()
            else:
                self.algorithm = self.DEFAULT_ALGORITHM

            if self.algorithm in self.HYBRID_ALGORITHMS:
                self.optimizer = optimizer or self.DEFAULT_OPTIMIZER
                self.optimizer_params = optimizer_params or \
                    self.OPTIMIZER_PARAMS.get(self.DEFAULT_OPTIMIZER, self.DEFAULT_OPTIMIZER_PARAMS)

                # The sampler and algorithm are correct for a hybrid algorithm, and the user passed in optimizer and
                # param args.
                # Now check to make sure these are legit. We need to parse the output of scipy's show_method.
                # Make sure that optimizer is in our available algorithms
                self.__check_optimizer()
                # Make sure that the optimizer params are correctly type
                self.__check_optimizer_params()

            # If user sends in an unrecognized algorithm, throw an exception
            else:
                raise ValueError(f"Sampler ({self.sampler}) and algorithm ({self.algorithm}) incompatible. "
                                 f"Make sure that the sampler is compatible with hybrid (variational) algorithms.")

            if self.sampler.startswith('braket'):
                self._set_braket_device()
                self._set_arn()

        # select quantum computer that is not for hybrid/variational algorithms. Eg., annealer like D-Wave.
        elif self.sampler in set(self.samplers[self.samplers['quantum'] & ~self.samplers['hybrid']]['target_name']):
            if algorithm:
                warn(f"Annealing sampler {self.sampler} does not utilize an algorithm argument. "
                     f"You passed {algorithm}", UserWarning)
            elif optimizer:
                warn(f"Annealing sampler {self.sampler} does not utilize an optimizer argument. "
                     f"You passed '{optimizer}'", UserWarning)

            if self.sampler.startswith('braket'):
                self._set_braket_device()
                self._set_arn()

        # We've fallen through  all quantum and hybrid options
        else:
            self.sampler = 'csample'

    @property
    def arn(self):
        return self._arn

    @arn.setter
    def arn(self, value):
        self._arn = value

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        self._device = value

    def __check_optimizer(self):
        """Make sure that optimizer is in our available algorithms"""
        assert isinstance(self.optimizer, str), "Parameter 'optimizer' must be of type str."
        if self.sampler.startswith('braket'):
            if self.optimizer.lower() not in get_scipy_minimize_methods():
                raise ValueError(f"Unknown optimizer. Parameter 'optimizer' must be one of "
                                 f"{get_scipy_minimize_methods()}")
        return True

    def __check_optimizer_params(self):
        assert isinstance(self.optimizer_params, dict), "Parameter 'optimizer_params' must be of type dictionary."
        return True

    def _check_sampler_type_is_qpu(self) -> bool:
        return self.sampler in set(self.samplers[self.samplers['quantum']]['target_name'])

    def _check_optimizer_has_params(self) -> bool:
        return self.optimizer is not None or self.optimizer_params is not None

    def get_device_and_models(self):
        # we only need one device name, the rest are repeats
        device_names = self.samplers[self.samplers['target_name'] == self.sampler]['device'].tolist()[0]
        models = self.samplers[self.samplers['target_name'] == self.sampler]['model'].tolist()
        return device_names, models

    def _set_braket_device(self):
        device_name, models = self.get_device_and_models()
        token = self.get_token()
        resp = self.check_braket_status(device_name, models, token)
        self.device = AwsDeviceClient.from_braket_check(resp)

        print(f"Set quantum device to {self.device.name}")
        assert self.device.status == self.BRAKET_ONLINE, f"No available devices for {self.sampler} sampler type."

    def confirm_qpu_execution(self, text):
        capture = input(text)
        if capture == 'n' or capture == 'N':
            print("Exiting...")
            sys.exit(0)
        else:
            print(f"You entered '{capture}'. Continuing...")

    def _set_arn(self):
        if not self.device:
            raise DeviceUnreachableException(f"There are no available devices for {self.sampler} sampler type.")
        self.arn = self.device.arn

    def is_quantum(self):
        return self._check_sampler_type_is_qpu() or self.is_hybrid()

    def is_hybrid(self):
        return self.sampler in set(self.samplers[self.samplers['hybrid']]['target_name'])

    def _check_size(self, obj) -> bool:
        if not self._check_problem_size(obj):
            qubit_count = self.samplers[self.samplers['model'] == self.device.name]['max_size'].item()
            raise ValueError(f"Problem size exceeds the number of qubits or variables available "
                             f"for the QPU, {self.sampler}. Maximum number of qubits = {qubit_count}")
        # make sure if a DW problem is solving a complete graph that it
        elif 'dwave' in self.sampler:
            # returns True if nqubits < max, raises value error otherwise
            print("Checking basic size thresholds for D-Wave QPUs...")
            return check_dwave_size(obj, self.device)
        else:
            return True

    def _check_problem_size(self, qubo: Union[dict, sp.spmatrix, np.ndarray]) -> bool:
        """
        Confirm whether sampler is a QPU and if so, whether size of qubo aligns
        with the number of qubits provided bythe QPU.

        :param qubo:  Union[dict, sp.spmatrix, np.ndarray]

        :return: bool
        """
        if self.device is not None:
            qubit_count = self.samplers[self.samplers['model'] == self.device.name]['max_size'].item()
        else:
            qubit_count = self.samplers[self.samplers['target_name'] == self.sampler]['max_size'].item()
        if isinstance(qubo, dict):
            n_qubits = len([key for key in qubo.keys() if key[0] == key[1]])
            return n_qubits <= qubit_count
        else:
            return qubo.shape[0] <= qubit_count

    def _get_data_type(self, data) -> str:
        if isinstance(data, dict):
            return 'dict'
        elif isinstance(data, np.ndarray):
            return 'dense'
        elif isinstance(data, nx.Graph):
            return 'graph'
        elif isinstance(data, sp.spmatrix):
            return 'sparse'
        else:
            raise TypeError('Unknown data type {}. Must pass dictionary, np.ndarray, '
                            'scipy sparse matrix, or NetworkX Graph'.format(type(data)))

    def get_available_samplers(self) -> None:
        """
        Provide a list of the available samplers.

        :return: List of samplers available to users.
        """
        print_available_samplers()

    def process_metadata(self, problem_type, data) -> dict:
        """
        Formulate the metadata dictionary based on input parameters and user input. We need to inform the backend
        services what type of problem we want to solve, the type of data sent, what sampler to use, and (optionally)
        the shape of the data so an encoded matrix can be reconstructed on the server side.

        :param problem_type: str, one of 'qubo', 'constraint_problem', 'lagrange_opt', 'graph'
        :param data:

        :return: dict with {problem_type, data_type, sampler, [shape]}
        """
        assert problem_type in self.PROBLEM_TYPES, \
            ValueError('Problem type must be one of {}'.format(self.PROBLEM_TYPES))
        m = {'problem_type': problem_type,
             'data_type': self._get_data_type(data),
             'sampler': self.sampler}
        if isinstance(data, np.ndarray) or isinstance(data, sp.spmatrix):
            m['shape'] = data.shape
        return encode_data(m)

    def process_params(self, params):

        quantum = self.sampler != 'csample'
        if not param_check(params, quantum=quantum):
            raise ValueError(f"Unknown parameter error. Please check kwargs. {params}")
        return encode_data(params)

    @staticmethod
    def process_data(data: Union[dict, np.ndarray, sp.spmatrix, nx.Graph]) -> Union[bytes, dict]:
        """
        Process the input data by encoding it.

        :param data: dict, np.ndarray, sp.spmatrix, nx.Graph,

        :return: Union[bytes, dict]. Encoded data, either dict with {'data': base64 encoded data object} or
            byte string encoding a NPTZ file obj.
        """
        if isinstance(data, dict):
            return {'data': encode_data(data)}
        elif isinstance(data, nx.Graph):
            return encode_graph(data)
        elif isinstance(data, np.ndarray):
            # byte string of a savez_compressed array
            return encode_ndarray(data)
        elif isinstance(data, sp.spmatrix):
            data = sp.coo_matrix(data, dtype=float)
            # byte string of a savez_compressed array
            return encode_sparse_array(data)
        else:
            raise TypeError("Input data must be dictionary, np.ndarray, or scipy.spmatrix")


class DeviceUnreachableException(Exception):
    """
    Raise when a device is offline.
    """
    pass
