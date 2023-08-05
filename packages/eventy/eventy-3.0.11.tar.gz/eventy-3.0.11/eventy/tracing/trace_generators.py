# Copyright (c) Qotto, 2021

"""
Trace IDs generation utilities
"""

import logging
from base64 import b64encode
from datetime import datetime, timezone
from secrets import token_urlsafe

logger = logging.getLogger(__name__)


class TraceGenerator:
    """
    Trace generator interface
    """

    def generate_trace(self, **kwargs):
        """
        Generate a trace id depending on keyword arguments

        :param kwargs: keyword arguments to define the trace
        :return: a new trace id
        """
        raise NotImplementedError


def _generate_encoded_date():
    ts_now = datetime.now(timezone.utc).timestamp()
    ts_2k = datetime(2000, 1, 1, tzinfo=timezone.utc).timestamp()
    ts2000res65536 = int(65536 * (ts_now - ts_2k)).to_bytes(6, 'big')
    encoded_date = b64encode(ts2000res65536, b'_-').decode('ascii')
    return encoded_date


def _generate_random(nbytes: int = 3):
    random = token_urlsafe(nbytes)
    return random


def _generate_trace(prefix: str, content: str):
    encoded_date = _generate_encoded_date()
    random = _generate_random(3)
    if prefix:
        prefix_str = f'{prefix}:'
    else:
        prefix_str = ''
    if content:
        content_str = f'{content}:'
    else:
        content_str = ''
    trace = f'{prefix_str}{content_str}{encoded_date}:{random}'
    logger.debug(f'Generated trace: {trace}')
    return trace


class FuncNameTraceGenerator(TraceGenerator):
    """
    Trace generator from a ``func_name``
    """

    def __init__(self, prefix: str = None):
        """
        Initialize the generator with a prefix

        :param prefix: prefix to be placed at the beginning of every trace ids
        """
        self.prefix = prefix

    def generate_trace(self, func_name=None, **kwargs):
        """
        Generate a trace depending on a function name

        :param func_name: function name
        :param kwargs: other keyword args are ignored
        :return: a new trace id "prefix:func_name:encoded_date:random"
        """
        return _generate_trace(self.prefix, func_name)
