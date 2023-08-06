# Copyright (c) Qotto, 2021

"""
Trace variables definition

Define TraceVar for trace ids: correlation_id and request_id
"""

from contextvars import ContextVar

TraceVar = ContextVar

correlation_id_var: TraceVar = TraceVar("correlation_id", default='')
"""
correlation_id trace var

>>> from eventy.tracing import correlation_id_var
>>> correlation_id_var.set('my_operation_using_many_services')
>>> print(correlation_id_var.get())
'my_operation_using_many_services'
"""

request_id_var: TraceVar = TraceVar("request_id", default='')
"""
request_id trace var

>>> from eventy.tracing import request_id_var
>>> request_id_var.set('my_service_request')
>>> print(request_id_var.get())
'my_service_request'
"""
