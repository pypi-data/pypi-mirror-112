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
from uuid import uuid4

from celery import shared_task as original_shared_task
from celery.execute import send_task as original_send_task
from celery.result import AsyncResult

from .common import DecoratorType
from ..tracing import correlation_id_var, request_id_var

logger = logging.getLogger(__name__)

__all__ = [
    'send_task',
    'shared_task',
    'with_namespace',
]


def send_task(name: str, args: List = [], kwargs: Dict = {}, **options) -> AsyncResult:
    """
    Modified version of celery.execute.send_task adding context in task kwargs

    options ar propagated as celery send_task named arguments and keyword arguments

    TODO: shouldn't we match argument names?
    ref: https://github.com/celery/celery/blob/494cc5d67452038c9b477d41cb2760b33ab4d5b8/celery/app/base.py#L704

    Usage::

        from eventy.integration.celery import send_task

        send_task(
            'service.task.name', [],
            {
                'param': 'value',
            }
        )

    Is equivalent to::

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
    if correlation_id_var.get():
        kwargs.update(correlation_id=correlation_id_var.get())
        logger.debug('Added correlation_id in task kwargs')
    else:
        logger.debug('No correlation_id in context to add in task kwargs')

    return original_send_task(name, args, kwargs, **options)


def shared_task(_func=None, **kwargs) -> DecoratorType:
    """
    Modified version of celery.shared_task fetching correlation id and generating request_id

    Usage::

        from eventy.integration.celery import shared_task

    Instead of::

        from celery import shared_task

    And then::

        @shared_task(options...)
        def my_task(param):
            pass


    :param _func: if used as a decorator with no args, decorated function will be first arg
    :param kwargs: optional ``namespace``, other options are propagated to celery's shared_task
    :return: new version of shared_task
    """

    def shared_task_decorator(function: Callable):

        @wraps(function)
        def decorated_shared_task(*func_args, **func_kwargs):
            if 'namespace' in kwargs:
                kwargs.update(name=f'{kwargs.pop("namespace")}.{function.__name__}')
            task_function = original_shared_task(**kwargs)(function)

            def inner():
                if 'correlation_id' in func_kwargs:
                    correlation_id_var.set(func_kwargs.pop('correlation_id'))
                else:
                    correlation_id_var.set(f'C:{function.__module__}.{function.__name__}:{uuid4()}')
                request_id_var.set(f'R:{function.__module__}.{function.__name__}:{uuid4()}')

                return task_function(*func_args, **func_kwargs)

            context = copy_context()
            result = context.run(inner)
            return result

        return decorated_shared_task

    if _func:
        # @shared_task
        # def f():
        return shared_task_decorator(_func)
    else:
        # @shared_task(param=value)
        # def f():
        return shared_task_decorator


def with_namespace(namespace: str, decorator: DecoratorType):
    """
    shared_task decorator factory adding namespace in task name

    Usage::

        from eventy.integration.celery import shared_task, with_namespace

        namespaced_shared_task = with_namespace('my_namespace', shared_task)

        @namespaced_shared_task(options...)
        def my_task(params...):
            pass

    :param namespace: namespace to configure the decorator with
    :param decorator: decorator to configure
    :return:
    """

    def decorator_with_namespace(_func=None, **kwargs):
        kwargs.update(namespace=namespace)
        return decorator(_func, **kwargs)

    return decorator_with_namespace
