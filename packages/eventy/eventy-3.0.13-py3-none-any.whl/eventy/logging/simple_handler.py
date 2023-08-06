# Copyright (c) Qotto, 2021

"""
Simple logging handler
----------------------

>>> import sys
>>> import logging
>>> logger = logging.getLogger('my_logger')
>>> logger.setLevel('DEBUG')
>>> handler = SimpleHandler(stream=sys.stdout)
>>> logger.addHandler(handler)
>>> logger.info('test')
[...] [CID:] [RID:] INFO my_logger (<doctest eventy.logging L1) test
"""

from logging import Formatter, StreamHandler

from coloredlogs import ColoredFormatter

from .trace_filters import add_correlation_id_filter, add_request_id_filter


class SimpleHandler(StreamHandler):
    """
    Simple logging handler, extending StreamHandler with optional colors and context information
    """

    def __init__(
        self,
        fmt='%(asctime)s [CID:%(correlation_id)s] [RID:%(request_id)s] '
            '%(levelname)s %(name)s (%(module)s L%(lineno)d) '
            '%(message)s',
        datefmt='[%Y-%m-%d %H:%M:%S %z]',
        colored=False,
        stream=None,
        level='DEBUG',
    ):
        """
        Initialize the handler

        :param fmt: Format string, can use the ``correlation_id`` and ``request_id`` fields for the log record
        :param datefmt: Date format string
        :param colored: Output colored messages (depending on log level)
        :param stream: output stream, default None, propagated to StreamHandler.__init__
        :param level: log level, default 'DEBUG', should be less than Logger.setLevel()
        """
        super().__init__(stream)
        self.addFilter(add_correlation_id_filter)
        self.addFilter(add_request_id_filter)
        if colored:
            self.setFormatter(ColoredFormatter(fmt=fmt, datefmt=datefmt))
        else:
            self.setFormatter(Formatter(fmt=fmt, datefmt=datefmt))
        self.setLevel(level=level)
