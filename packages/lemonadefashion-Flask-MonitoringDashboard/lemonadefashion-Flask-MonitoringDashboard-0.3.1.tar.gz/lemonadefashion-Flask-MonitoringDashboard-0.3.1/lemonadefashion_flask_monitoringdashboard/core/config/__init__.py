try:
    import configparser
except ImportError:
    configparser = None

import os

import pytz
from tzlocal import get_localzone

from lemonadefashion_flask_monitoringdashboard.core.config.parser import (
    parse_string,
    parse_version,
    parse_bool,
    parse_literal,
)
from lemonadefashion_flask_monitoringdashboard.core.logger import log


class Config(object):
    """
        The settings can be changed by setting up a config file. For an example of a config file,
        see config.cfg in the main-directory.
    """

    def __init__(self):
        """Sets the default values for the project."""
        # dashboard
        self.version = '1.0'
        self.blueprint_name = 'dashboard'
        self.scheme = 'http'
        self.host = None
        self.link = 'dashboard'
        self.monitor_level = 1
        self.outlier_detection_constant = 2.5
        self.sampling_period = 5 / 1000.0
        self.enable_logging = False

        # database
        self.database_name = 'sqlite:///flask_monitoringdashboard.db'
        self.table_prefix = ''

        # authentication
        self.username = 'admin'
        self.password = 'admin'
        self.security_token = 'cc83733cb0af8b884ff6577086b87909'

        # visualization
        self.colors = {}
        try:
            self.timezone = pytz.timezone(str(get_localzone()))
        except pytz.UnknownTimeZoneError:
            log('Using default timezone, which is UTC')
            self.timezone = pytz.timezone('UTC')

        # define a custom function to retrieve the session_id or username
        self.group_by = None

        # store the Flask app
        self.app = None

        # dependencies
        self.get_ip = None

    def inject_dependencies(self, get_ip=None):
        """
            Injects certain dependencies into the Monitoring Dashboard for better integration.
            :param get_ip: a function that gets the appropriate client IP address inside a request
                context. Overriding this allows you to provide the correct IP for logging purposes
                in case your setup is running behind reverse proxies.
        """
        if get_ip:
            self.get_ip = get_ip

    def init_from(self, file=None, envvar=None, config=None, log_verbose=False):
        """
            The config_file must at least contains the following variables in section 'dashboard':
            - APP_VERSION: the version of the app that you use. Updating the version helps in
                showing differences in execution times of a function over a period of time.
            - GIT = If you're using git, then it is easier to set the location to the .git-folder,
                The location is relative to the config-file.
            - BLUEPRINT_NAME: The name of the blueprint the FMD adds to the Flask app.
                default: "dashboard"
            - SCHEME: What scheme should be used for URLs?
            - HOST: The dashboard will use this host.
            - CUSTOM_LINK: The dashboard can be visited at {HOST}/{CUSTOM_LINK}.
            - MONITOR_LEVEL: The level for monitoring your endpoints. The default value is 3.
            - OUTLIER_DETECTION_CONSTANT: When the execution time is more than this constant *
                average, extra information is logged into the database. A default value for this
                variable is 2.5.
            - SAMPLING_PERIOD: Time between two profiler-samples. The time must be specified in ms.
                If this value is not set, the profiler continuously monitors.
            - ENABLE_LOGGING: Boolean if you want additional logs to be printed to the console.
            Default value is False

            The config_file must at least contains the following variables in section
            'authentication':
            - USERNAME: for logging into the dashboard, a username and password is required. The
                username can be set using this variable.
            - PASSWORD: same as for the username, but this is the password variable.
            - SECURITY_TOKEN: Used for getting the data in /get_json_data

            The config_file must at least contains the following variables in section 'database':
            - DATABASE: Suppose you have multiple projects where you're working on and want to
                separate the results. Then you can specify different database_names, such that the
                result of each project is stored in its own database.
            - TABLE_PREFIX: A prefix to every table that the Flask-MonitoringDashboard uses, to
                ensure that there are no conflicts with the user of the dashboard.

            The config_file must at least contains the following variables in section
            'visualization':
            - TIMEZONE: The timezone for converting a UTC timestamp to a local timestamp.
                for a list of all timezones, use the following:

                >>> import pytz  # pip install pytz
                >>> print(pytz.all_timezones)

            - COLORS: A dictionary to override the colors used per endpoint.

            :param file: a string pointing to the location of a config-file.
            :param envvar: a string specifying which environment variable holds the config file
                location.
            :param config: an object containing the configuration directly.
            :param log_verbose: flag to print the location of the config file.
        """
        if (config and file and envvar) or (config and file) or (config and envvar) or (file and envvar):
            raise Exception("You can only pass one of config, file and envvar.")

        if envvar:
            file = os.getenv(envvar)
            if log_verbose:
                log("Running with config from: " + (str(file)))

        if not config and not file:
            # Travis does not need a config file.
            if '/home/travis/build/' in os.getcwd():
                return
            log("No configuration file or object specified. Please do so.")
            return

        if file:
            try:
                parser = configparser.RawConfigParser()
                parser.read(file)

                # parse 'dashboard'
                self.version = parse_version(parser, 'dashboard', self.version)
                self.blueprint_name = parse_string(parser, 'dashboard', 'BLUEPRINT_NAME', self.blueprint_name)
                self.scheme = parse_string(parser, 'dashboard', 'SCHEME', self.scheme)
                self.host = parse_string(parser, 'dashboard', 'HOST', self.host)
                self.link = parse_string(parser, 'dashboard', 'CUSTOM_LINK', self.link)
                self.monitor_level = parse_literal(parser, 'dashboard', 'MONITOR_LEVEL', self.monitor_level)
                self.outlier_detection_constant = parse_literal(
                    parser, 'dashboard', 'OUTLIER_DETECTION_CONSTANT', self.outlier_detection_constant)
                self.sampling_period = (
                    parse_literal(parser, 'dashboard', 'SAMPLING_RATE', self.sampling_period) / 1000.0)
                self.enable_logging = parse_bool(parser, 'dashboard', 'ENABLE_LOGGING', self.enable_logging)

                # parse 'authentication'
                self.username = parse_string(parser, 'authentication', 'USERNAME', self.username)
                self.password = parse_string(parser, 'authentication', 'PASSWORD', self.password)
                self.security_token = parse_string(parser, 'authentication', 'SECURITY_TOKEN', self.security_token)

                # database
                self.database_name = parse_string(parser, 'database', 'DATABASE', self.database_name)
                self.table_prefix = parse_string(parser, 'database', 'TABLE_PREFIX', self.table_prefix)

                # visualization
                self.colors = parse_literal(parser, 'visualization', 'COLORS', self.colors)
                self.timezone = pytz.timezone(parse_string(parser, 'visualization', 'TIMEZONE', self.timezone.zone))

                if log_verbose:
                    log("version: " + self.version)
                    log("username: " + self.username)
            except AttributeError:
                log('Cannot use configparser in python2.7')
                raise

        if config:
            try:
                if 'version' in config:
                    self.version = config['version']
                if 'blueprint_name' in config:
                    self.blueprint_name =  config['blueprint_name']
                if 'scheme' in config:
                    self.scheme = config['scheme']
                if 'host' in config:
                    self.host = config['host']
                if 'link' in config:
                    self.link = config['link']
                if 'monitor_level' in config:
                    self.monitor_level = config['monitor_level']
                if 'outlier_detection_constant' in config:
                    self.outlier_detection_constant = config['outlier_detection_constant']
                if 'sampling_period' in config:
                    self.sampling_period = config['sampling_period'] / 1000.0
                if 'enable_logging' in config:
                    self.enable_logging = config['enable_logging']

                if 'username' in config:
                    self.username = config['username']
                if 'password' in config:
                    self.password = config['password']
                if 'security_token' in config:
                    self.security_token = config['security_token']

                if 'database_name' in config:
                    self.database_name = config['database_name']
                if 'table_prefix' in config:
                    self.table_prefix = config['table_prefix']

                if 'colors' in config:
                    self.colors = config['colors']
                if 'timezone' in config:
                    self.timezone = pytz.timezone(config['timezone'])

                if log_verbose:
                    log("version: " + self.version)
                    log("username: " + self.username)
            except KeyError:
                log('Configuration object is missing something.')
                raise
