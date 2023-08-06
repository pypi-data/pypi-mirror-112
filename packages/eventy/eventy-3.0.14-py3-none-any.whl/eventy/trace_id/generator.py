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
    return f'{eventy.config.SERVICE_NAME}:{func.__name__}:{token_urlsafe(8)}'
