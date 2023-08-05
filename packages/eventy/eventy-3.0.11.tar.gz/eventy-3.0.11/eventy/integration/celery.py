# Copyright (c) Qotto, 2021

"""
Celery integration utilities
----------------------------

Utility functions to integrate the eventy protocol in celery apps

The celery module works best with celery optional dependencies installed ("pip install eventy[celery]")
"""

import logging
from typing import Callable, Any

from .common import DecoratorType, merge_decorators
from ..tracing import correlation_id_var

logger = logging.getLogger(__name__)

try:
    from celery.result import AsyncResult

    logger.debug("Celery support enabled")
except ImportError:
    AsyncResult = Any
    logger.debug("Celery support disabled")

__all__ = [
    'celery_traced_send_task',
    'celery_task_decorator',
]


def celery_traced_send_task(
    celery_send_task: Callable
) -> Callable[[str, list, dict, ], AsyncResult]:
    """
    Wraps a celery send_task method, adding tracing information to task_kwargs

    Configure::

        from eventy.integration.celery import celery_traced_send_task
        from celery.execute import send_task
        traced_send_task = celery_traced_send_task(send_task)

    Then::

        traced_send_task('service.task.name', [], {param=value})

    Is equivalent to::

        send_task(('service.task.name', [], {param=value, correlation_id=correlation_id_ctx.get()})

    The returned method has the following signature::

        traced_send_task(task_name: str, task_args: list, task_kwargs: dict, **celery_options) -> AsyncResult

    Where optional ``**celery_options`` are propagated to celery's send_task

    :param celery_send_task: send_task method from celery. Can be celery.execute.send_task, or Celery app.send_task
    :return: wrapped send_task method automatically including correlation_id in task kwargs
    """

    def traced_send_task(task_name: str, task_args: list, task_kwargs: dict, **celery_options) -> AsyncResult:
        """
        Modified version of celery.execute.send_task adding context in task kwargs
        """
        if correlation_id_var.is_defined():
            task_kwargs.update(correlation_id=correlation_id_var.get())
            logger.debug('Added correlation_id in task kwargs')
        else:
            logger.debug('No correlation_id in context to add in task kwargs')

        return celery_send_task(task_name, task_args, task_kwargs, **celery_options)

    return traced_send_task


def celery_task_decorator(
    celery_decorator,
    namespace: str = "",
    *other_decorators
) -> DecoratorType:
    """
    Decorator factory wrapping celery task and share_task decorators to include namespace in task name

    Configuration::

        from eventy.integration.celery import celery_task_decorator
        from eventy.integration.common import trace_decorator
        from eventy.tracing import correlation_id_var, FuncNameTraceGenerator

        shared_task = celery_task_decorator(
            celery.shared_task,
            'my_service_tasks_namespace',
            trace_decorator(
                correlation_id_var,
                FuncNameTraceGenerator('my_operation_correlation_namespace'),
                fetch=True, override=False,
        )

    Usage is then straightforward::

        @shared_task
        def my_task(param):
            pass


    :param celery_decorator: celery task decorator to modify
    :param namespace: namespace to prefix celery decorator name with
    :param other_decorators: optionally apply these before namespaced (e.g. for tracing)
    :return: a new decorator
    """

    def auto_decorator(*decorator_args, **decorator_kwargs) -> DecoratorType:
        logger.debug(
            f'namespaced {celery_decorator.__name__} decorator_args={decorator_args} - decorator_kwargs={decorator_kwargs}'
        )

        def decorator(func: Callable):
            def decorated_func(*func_args, **func_kwargs):
                full_name = f'{namespace}.tasks.{func.__name__}'
                decorator_kwargs.update(name=full_name)
                inner_func = merge_decorators(*other_decorators)(func)
                # > When using multiple decorators in combination with the task decorator
                # > you must make sure that the task decorator is applied last
                # https://docs.celeryproject.org/en/latest/userguide/tasks.html
                return celery_decorator(**decorator_kwargs)(inner_func)(*func_args, **func_kwargs)

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
