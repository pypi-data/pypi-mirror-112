# Copyright (c) Qotto, 2021

"""
Include support for context bound trace ids

* :obj:`trace_vars.correlation_id_var` a Correlation ID to correlate multiple services
  involved in the same business operation
* :obj:`trace_vars.request_id_var` a Request ID to identify a single request on a service

Include support to generate trace ids

* :class:`trace_generators.FuncNameTraceGenerator` trace id generator from a function name
"""

from .trace_generators import FuncNameTraceGenerator
from .trace_vars import correlation_id_var, request_id_var

__all__ = [
    'correlation_id_var',
    'request_id_var',
    'FuncNameTraceGenerator',
]
