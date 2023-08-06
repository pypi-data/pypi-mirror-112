# Copyright (c) Qotto, 2021

"""
Logging filters to inject trace ids in LogRecord instances
"""

from logging import LogRecord

from ..tracing import correlation_id_var, request_id_var


def add_correlation_id_filter(log_record: LogRecord) -> bool:
    log_record.correlation_id = correlation_id_var.get()  # type: ignore
    return True


def add_request_id_filter(log_record: LogRecord) -> bool:
    log_record.request_id = request_id_var.get()  # type: ignore
    return True
