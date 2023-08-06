# Copyright (c) Qotto, 2021

"""
Celery integration utilities

Utility functions to integrate the eventy protocol in celery apps

The celery module works best with celery optional dependencies installed ("pip install eventy[celery]")
"""

import logging
from contextvars import copy_context
from typing import Callable, List, Dict

from celery import shared_task as original_shared_task
from celery.execute import send_task as original_send_task
from celery.result import AsyncResult

from eventy.tracing.trace_generators import NamespaceNameTraceGenerator
from .common import DecoratorType
from ..tracing import TraceGenerator, correlation_id_var, request_id_var

logger = logging.getLogger(__name__)

__all__ = [
    'send_task',
    'task_decorator',
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


def task_decorator(
    original_task=original_shared_task,
    namespace='',
    correlation_id_generator: TraceGenerator = NamespaceNameTraceGenerator(),
    request_id_generator: TraceGenerator = NamespaceNameTraceGenerator(),
):
    """
    Modify celery @task and @shared_task to include namespace and traces

    Example::

        from celery import shared_task as original_shared_task
        from eventy.integration.celery import task_decorator

        shared_task = task_decorator(
            original_shared_task,
            'my.namespace',
        )

        @shared_task
        def my_task(param=value):
            pass

    :param original_task: original celery task (celery.shared_task or Celery app.task)
    :param namespace: namespace of the task
    :param correlation_id_generator: used to generate a correlation_id if not in kwargs, from ``namespace`` and ``name`` (set to function __name__)
    :param request_id_generator: always used to generate a request_id, from ``namespace`` and ``name`` (set to function __name__)
    :return: a new decorator, can be further configured with celery options
    """

    def auto_decorator(*decorator_args, **decorator_kwargs) -> DecoratorType:
        logger.debug(
            f'namespaced {original_task.__name__} decorator_args={decorator_args} - decorator_kwargs={decorator_kwargs}'
        )

        def decorator(func: Callable):
            def decorated_func(*func_args, **func_kwargs):
                full_name = f'{namespace}.tasks.{func.__name__}'
                decorator_kwargs.update(name=full_name)
                # > When using multiple decorators in combination with the task decorator
                # > you must make sure that the task decorator is applied last
                # https://docs.celeryproject.org/en/latest/userguide/tasks.html
                task_func = original_task(**decorator_kwargs)(func)

                def inner():
                    request_id = request_id_generator.generate_trace(namespace=namespace, name=func.__name__)
                    if 'correlation_id' in func_kwargs:
                        correlation_id = func_kwargs.pop('correlation_id')
                    else:
                        correlation_id = correlation_id_generator.generate_trace(
                            namespace=namespace, name=func.__name__
                        )

                    request_id_var.set(request_id)
                    correlation_id_var.set(correlation_id)
                    return task_func(*func_args, **func_kwargs)

                context = copy_context()
                result = context.run(inner)
                return result

            return decorated_func

        if len(decorator_args) == 1 and callable(decorator_args[0]):
            # @decorator
            # def f():
            return decorator(decorator_args[0])
        else:
            # @decorator(param=value)
            # def f():
            return decorator

    return auto_decorator
