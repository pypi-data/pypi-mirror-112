# Copyright (c) Qotto, 2021

"""
Celery integration utilities

Utility functions to integrate the eventy protocol in celery apps

The celery module only works with celery optional dependencies installed ("pip install eventy[celery]")
"""
import logging

logger = logging.getLogger(__name__)

try:
    from ._celery import task_decorator, send_task

    task_decorator.__module__ = 'eventy.integration.celery'
    send_task.__module__ = 'eventy.integration.celery'

    __all__ = [
        'task_decorator',
        'send_task',
    ]

    print('Celery support enabled')

except ImportError:
    print('Celery support disabled')
