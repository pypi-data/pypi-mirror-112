import json
import inspect
import logging
import os

from google.cloud import logging as cloudlogging

CLOUD_LOGGER_NAME = os.environ.get('CLOUD_LOGGER_NAME')
SENTRY_DSN = os.environ.get('SENTRY_DSN')
ENV = os.environ.get("ENV", "developmebt")


class CustomFormatter(logging.Formatter):
    def format(self, record):
        logmsg = super(CustomFormatter, self).format(record)
        try:
            return json.loads(logmsg)
        except:
            return logmsg


if not CLOUD_LOGGER_NAME:
    raise AttributeError("Cannot instantiate module without the CLOUD_LOGGER_NAME environment variable set. "
                         "Explicitly create the variable and re-run the application")

try:
    log_client = cloudlogging.Client()
    log_handler = log_client.get_default_handler()
    log_handler.setFormatter(CustomFormatter())
    cloud_logger = logging.getLogger(CLOUD_LOGGER_NAME)
    cloud_logger.setLevel(logging.INFO)
    cloud_logger.addHandler(log_handler)
except Exception as e:
    raise Exception('Cannot instantiate the cloud logger', e.args)


def get_executed_method():
    return inspect.stack()[2][3]


def info(*args, **kwargs):
    if len(args) == 1:
        cloud_logger.info(args[0])
        return
    message = json.dumps({"data": {**kwargs}, "method": get_executed_method()})
    cloud_logger.info(message)


def warning(*args, **kwargs):
    if len(args) == 1:
        cloud_logger.warning(args[0])
        return
    message = json.dumps({"data": {**kwargs}, "method": get_executed_method()})
    cloud_logger.warning(message)


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
