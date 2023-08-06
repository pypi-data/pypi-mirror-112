# Copyright (c) Qotto, 2021

"""
Celery integration utilities

Utility functions to integrate the eventy protocol in celery apps

The celery module works best with celery optional dependencies installed ("pip install eventy[celery]")
"""

import logging
from contextvars import copy_context
from functools import wraps
from typing import Callable, List, Dict

from celery import shared_task as original_shared_task
from celery.execute import send_task as original_send_task
from celery.result import AsyncResult

from eventy.trace_id import correlation_id_var, request_id_var
from eventy.trace_id.generator import gen_trace_id

logger = logging.getLogger(__name__)

__all__ = [
    'send_task',
    'shared_task',
]


def send_task(name: str, args: List = None, kwargs: Dict = None, **options) -> AsyncResult:
    """
    Modified version of celery.execute.send_task adding context in task kwargs

    options ar propagated as celery send_task named arguments and keyword arguments

    Usage::

        from eventy.integration.celery import send_task

        send_task(
            'service.task.name', [],
            {
                'param': 'value',
            }
        )

    If a correlation_id is defined in the current context, it is equivalent to::

        from celery.execute import send_task
        from eventy.tracing import correlation_id_var

        send_task(
            'service.task.name', [],
            {
                'correlation_id': correlation_id_var.get(),
                'param': 'value',
            }
        )
    """
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    if correlation_id_var.get():
        kwargs.update(correlation_id=correlation_id_var.get())

    return original_send_task(name, args, kwargs, **options)


def _extracting_trace_id(func: Callable) -> Callable:
    """
    Decorate a function so that it extract correlation_id and generate request_id

    :param func: function to modify
    :return: a new function extracting trace ids
    """

    @wraps(func)
    def inner(*args, **kwargs):
        logger.debug(f'xtract 1 {args} / {kwargs}')
        if 'correlation_id' in kwargs:
            correlation_id_var.set(kwargs.pop('correlation_id'))
        else:
            correlation_id_var.set(gen_trace_id(func))
        request_id_var.set(gen_trace_id(func))

        logger.debug(f'xtract 2 {args} / {kwargs}')
        return func(*args, **kwargs)

    return inner


def _running_in_context(func: Callable) -> Callable:
    """
    Decorate a function so that it runs in a new stacked context

    Modification to context variables will be bound to the execution of the function
    :param func: function to run in context
    :return: a new function running in its own context
    """

    @wraps(func)
    def inner(*args, **kwargs):
        logger.debug(f'context {args} / {kwargs}')

        def inner_in_context():
            return func(*args, **kwargs)

        context = copy_context()
        return context.run(inner_in_context)

    return inner


def shared_task(_func: Callable = None, **kwargs) -> Callable:
    """
    Modified version of celery.shared_task adding traces in the task keyword arguments

    ``correlation_id`` is fetched from context, or generated. ``request_id`` is always generated

    Usage::

        from eventy.integration.celery import shared_task

    Instead of::

        from celery import shared_task

    And then::

        @shared_task(options...)
        def my_task(param):
            ...


    :param _func: if used as a decorator with no args, decorated function will be first arg
    :param kwargs: options are propagated to celery's shared_task
    :return: new version of shared_task
    """

    def shared_task_decorator(func: Callable) -> Callable:
        return original_shared_task(**kwargs)(
            _running_in_context(
                _extracting_trace_id(
                    func
                )
            )
        )

    if _func:
        # @shared_task
        # def f():
        return shared_task_decorator(_func)
    else:
        # @shared_task(param=value)
        # def f():
        return shared_task_decorator
