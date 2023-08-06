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


class NamespaceNameDateRandomTraceGenerator(TraceGenerator):
    def generate_trace(self, namespace: str = '', name: str = '', date: str = '', random: str = '', **kwargs):
        return f'{namespace}:{name}:{date}:{random}'


def _generate_encoded_date():
    ts_now = datetime.now(timezone.utc).timestamp()
    ts_2k = datetime(2000, 1, 1, tzinfo=timezone.utc).timestamp()
    ts2000res65536 = int(65536 * (ts_now - ts_2k)).to_bytes(6, 'big')
    encoded_date = b64encode(ts2000res65536, b'_-').decode('ascii')
    return encoded_date


def _generate_random(nbytes: int = 3):
    random = token_urlsafe(nbytes)
    return random


class NamespaceNameTraceGenerator(TraceGenerator):
    """
    Trace generator from a ``namespace`` and ``func_name``
    """

    def generate_trace(self, namespace=None, name=None, **kwargs):
        """
        Generate a trace depending on a function name in a namespace

        :param namespace: function name
        :param name: function name
        :param kwargs: other keyword args are ignored
        :return: a new trace id "prefix:func_name:encoded_date:random"
        """
        return NamespaceNameDateRandomTraceGenerator().generate_trace(
            namespace=namespace,
            name=name,
            date=_generate_encoded_date(),
            random=_generate_random(),
        )
