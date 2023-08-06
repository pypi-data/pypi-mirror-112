import json
import inspect
import logging
import os
from google.cloud import logging as cloudlogging

CLOUD_LOGGER_NAME = os.environ.get("CLOUD_LOGGER_NAME")

if not CLOUD_LOGGER_NAME:
    raise AttributeError(
        "Cannot instantiate module without the CLOUD_LOGGER_NAME environment variable set. "
        "Explicitly create the variable and re-run the application"
    )


class FallbackCloudLogger:
    def __init__(self):
        logging.basicConfig(level=logging.NOTSET)
        self.logger = logging.getLogger('root')
        self.logger.setLevel(logging.DEBUG)

    def log_struct(self, dict, severity="INFO"):
        data = json.dumps(dict, indent=4)

        if severity == "INFO":
            self.logger.info(data)
        if severity == "WARNING":
            self.logger.warning(data)

    def log_text(self, message, severity="INFO"):
        if severity == "INFO":
            self.logger.info(message)
        if severity == "WARNING":
            self.logger.warning(message)


try:
    log_client = cloudlogging.Client()
    log_client.get_default_handler()
    log_client.setup_logging()
    cloud_logger = log_client.logger(CLOUD_LOGGER_NAME)
except Exception as e:
    cloud_logger = FallbackCloudLogger()


def get_executed_method():
    return inspect.stack()[2][3]


def info(*args, **kwargs):
    if len(args) == 1:
        cloud_logger.log_text(args[0], severity="INFO")
        return
    cloud_logger.log_struct(
        {**kwargs, "method": get_executed_method()}, severity="INFO"
    )


def warning(*args, **kwargs):
    if len(args) == 1:
        cloud_logger.log_text(args[0], severity="WARNING")
        return
    cloud_logger.log_struct(
        {**kwargs, "method": get_executed_method()}, severity="WARNING"
    )


def error(*args, **kwargs):
    if len(args) == 1:
        logging.error(args[0])
        return
    message = json.dumps({"data": {**kwargs}, "method": get_executed_method()})
    logging.error(message)


def exception(*args, **kwargs):
    if len(args) == 1:
        logging.exception(args[0])
        return
    message = json.dumps({"data": {**kwargs}, "method": get_executed_method()})
    logging.exception(message)
