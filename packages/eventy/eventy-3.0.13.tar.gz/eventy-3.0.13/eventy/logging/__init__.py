# Copyright (c) Qotto, 2021

"""
Provides logging handlers to integrate tracing in log messages.

Include a :class:`simple_hamdler.SimpleHandler`
and a Google Kubernetes Engines specific :class:`gke_handler.GkeHandler`
"""

from .trace_filters import add_correlation_id_filter, add_request_id_filter
from .gke_handler import GkeHandler
from .simple_handler import SimpleHandler

__all__ = [
    'add_correlation_id_filter',
    'add_request_id_filter',
    'SimpleHandler',
    'GkeHandler',
]
