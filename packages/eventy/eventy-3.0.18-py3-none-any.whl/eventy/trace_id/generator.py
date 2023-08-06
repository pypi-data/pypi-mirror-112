# Copyright (c) Qotto, 2021

"""
Trace IDs generation utilities
"""

from secrets import token_urlsafe
from typing import Callable

import eventy.config

__all__ = [
    'gen_trace_id',
]


def gen_trace_id(func: Callable) -> str:
    """
    Generate a trace id from a function

    Uses :obj:`eventy.config.SERVICE_NAME`, func __name__, and a random string
    :param func: function where the trace id is defined
    :return: a new trace id
    """
    return f'{eventy.config.SERVICE_NAME}:{func.__name__}:{token_urlsafe(8)}'
