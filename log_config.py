import logging
import uuid
from contextvars import ContextVar

# Create a context-local variable to hold the request ID
request_id_var = ContextVar("request_id")

# Define a custom logging class that retrieves the request ID from context-local storage
class RequestIdLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, **kwargs):
        if extra is None:
            extra = {}
        # Get the request ID from context-local storage, if it's set
        request_id = request_id_var.get(None)
        if request_id is not None:
            extra["request_id"] = request_id
        super()._log(level, msg, args, exc_info, extra, **kwargs)

def setup_logging():
    # Configure the logging system to use the custom logging class
    logging.setLoggerClass(RequestIdLogger)
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] - p%(process)s {%(pathname)s:%(lineno)d} - %(levelname)s - %(message)s'
    )
