# Copyright (c) Qotto, 2021

"""
Common integration utilities
----------------------------

Utility functions to integrate the eventy protocol in your workflow

Provides decorator factories to decorate functions and automatically extract tracing context
"""

import contextvars
import logging
from typing import Callable

from ..tracing.trace_generators import TraceGenerator
from ..tracing.trace_vars import TraceVar

logger = logging.getLogger(__name__)

__all__ = [
    'trace_decorator',
    'merge_decorators',
    'DecoratorType',
]

DecoratorType = Callable[..., Callable]


def merge_decorators(
    *decorators,
) -> DecoratorType:
    """
    Decorator factory merging multiple decorators, apply from left to right

    :param decorators: decorators to merge
    :return: a new decorator applying all decorators
    """

    if not decorators:
        def identity(func):
            return func

        return identity

    def decorator(func):
        def decorated_func(*args, **kwargs):
            inner_func = func
            nested_decorators = decorators
            for nested_decorator in nested_decorators:
                inner_func = nested_decorator(inner_func)

            return inner_func(*args, **kwargs)

        return decorated_func

    return decorator


def trace_decorator(
    trace_var: TraceVar,
    trace_generator: TraceGenerator,
    fetch: bool = True,
    override: bool = False,
) -> DecoratorType:
    """
    Decorator factory fetching trace from kwargs

    :param trace_var: TraceVar (correlation_id_var or request_id_var)
    :param trace_generator: TraceGenerator to generate trace id from function name func_name
    :param fetch: should the trace be fetched from decorated function kwargs?
    :param override: should the new trace override existing trace if present?
    :return: the configured decorator
    """

    def decorator(func):
        def decorated_func(*args, **kwargs):
            def inner():
                if trace_var.name in kwargs and fetch:
                    trace_id = kwargs.pop(trace_var.name)

                    if override or not trace_var.is_defined():
                        logger.debug(f'Will set {trace_var.name}={trace_id} from {func.__name__} kwargs')
                        trace_var.set(trace_id)

                    else:
                        logger.debug(f'Will not use {trace_var.name}={trace_id} from {func.__name__} kwargs')

                elif trace_generator:
                    trace_id = trace_generator.generate_trace(
                        func_name=func.__name__,
                        func_args=args, func_kwargs=kwargs
                    )

                    if override or not trace_var.is_defined():
                        logger.debug(f'Will set {trace_var.name}={trace_id} generated for {func.__name__}')
                        trace_var.set(trace_id)

                    else:
                        logger.debug(f'Will not use {trace_var.name}={trace_id} generated for {func.__name__}')

                return func(*args, **kwargs)

            context = contextvars.copy_context()
            result = context.run(inner)
            return result

        renamed_decorated_func = decorated_func
        renamed_decorated_func.__name__ = func.__name__
        return renamed_decorated_func

    return decorator
