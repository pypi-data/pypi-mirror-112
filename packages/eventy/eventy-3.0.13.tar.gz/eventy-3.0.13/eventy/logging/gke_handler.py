# Copyright (c) Qotto, 2021

"""
GKE logging handler
-------------------

>>> import sys
>>> import logging
>>> logger = logging.getLogger('my_logger')
>>> logger.setLevel('DEBUG')
>>> handler = GkeHandler(stream=sys.stdout)
>>> logger.addHandler(handler)
>>> logger.info('test')
{\
"timestamp": {"seconds": ..., "nanos": ...}, "severity": "INFO", "message": "test", \
"file": "<doctest eventy.logging.gke_handler[6]>", "line": 1, "module": "<doctest eventy.logging", \
"function": "<module>", "logger_name": "my_logger", "thread": ...\
}
"""

import json
import logging
import math

from .trace_filters import add_correlation_id_filter, add_request_id_filter


class GkeHandler(logging.StreamHandler):
    """
    GKE logging handler formats log message to Google Kubernetes Engine JSON format
    """

    def __init__(self, stream=None, level='DEBUG'):
        """
        Initialize the handler

        :param stream: output stream, default None, propagated to StreamHandler.__init__
        :param level: log level, default 'DEBUG', should be less than Logger.setLevel()
        """
        super().__init__(stream)
        self.addFilter(add_correlation_id_filter)
        self.addFilter(add_request_id_filter)
        self.setLevel(level=level)

    def format(self, record: logging.LogRecord) -> str:
        """
        Override default formatting create a JSON in GKE format

        :param record: log record to format
        :return: formatted JSON string
        """
        message = super().format(record)

        subsecond, second = math.modf(record.created)
        payload = {
            'timestamp': {'seconds': int(second), 'nanos': int(subsecond * 1e9)},
            'severity': record.levelname,
            'message': message,
            'file': record.pathname,
            'line': record.lineno,
            'module': record.module,
            'function': record.funcName,
            'logger_name': record.name,
            'thread': record.thread,
        }
        payload['correlation_id'] = record.correlation_id  # type: ignore
        payload['request_id'] = record.request_id  # type: ignore
        return json.dumps(payload)
