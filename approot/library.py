""" General purpose library constants and functions """

# import logging

# from logging.handlers import TimedRotatingFileHandler

from pathlib import Path
from configparser import ConfigParser


def get_config_section(section):
    """ Gets a section from the environment configuration file """

    config_parser = ConfigParser(interpolation=None)

    config_parser.read(PROJECT_DIR / 'environment.ini')

    return config_parser[section]


# def open_logger():
#     """ Initializes the application logger """

#     logging_settings = get_config_section('logging')

#     logger = logging.getLogger('default')

#     if DEBUG:
#         log_level = logging.DEBUG
#         log_entry = "Logging level is DEBUG"
#     else:
#         log_level = logging.INFO
#         log_entry = "Logging level is INFO"

#     logger.setLevel(log_level)

#     log_file_path = PROJECT_DIR / "logs/api.log"

#     file_handler = TimedRotatingFileHandler(
#         filename = log_file_path,
#         when = 'midnight',
#         interval = 1,
#         backupCount = logging_settings.getint('backup_count')
#     )

#     log_format = "%(asctime)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s"

#     logging_formatter = logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S")

#     file_handler.setFormatter(logging_formatter)

#     logger.addHandler(file_handler)

#     logger.info("-------------------- Starting program --------------------")
#     logger.info(log_entry)


# Constants
SIGNUP_SESSION_DURATION = 2 * 60
DEFAULT_SESSION_DURATION = 6 * 60

# Create directory references
APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = Path(APP_DIR).parent

# Get application settings
app_settings = get_config_section('application')

DEBUG = app_settings.getboolean('debug')
TITLE = app_settings['title']
ALLOWED_ORIGINS = app_settings['allowed_origins'].split(',')

# Get application secrets
app_secrets = get_config_section('secrets')

#SWEATSCORE_SECRET_KEY = bytes(app_secrets['secret_key'], encoding='utf-8')
SWEATSCORE_SECRET_KEY = app_secrets['secret_key']
