#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: notifierlib.py
#
# Copyright 2017 Costas Tyfoxylos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for notifierlib.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import abc
import logging
from queue import Queue
from threading import Thread

from stopit import ThreadingTimeout, TimeoutException


__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = '''google'''
__date__ = '''18-09-2017'''
__copyright__ = '''Copyright 2017, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<costas.tyf@gmail.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging
LOGGER_BASENAME = '''notifierlib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

WORKERS = 3
TIMEOUT = 30


class Channel:  # pylint: disable=too-few-public-methods
    """Interface for a channel."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self._logger = logging.getLogger('{base}.{suffix}'
                                         .format(base=LOGGER_BASENAME,
                                                 suffix=self.__class__.__name__))
        self.name = name

    @abc.abstractmethod
    def notify(self):
        """Notify implementation."""


class Group:
    """Models a group."""

    def __init__(self, group_name, *channels):
        self._logger = logging.getLogger('{base}.{suffix}'
                                         .format(base=LOGGER_BASENAME,
                                                 suffix=self.__class__.__name__)
                                         )
        self.name = group_name
        self._channels = [self._validate_channel(channel)
                          for channel in channels]
        self._queue = Queue()
        self._results = None

    @staticmethod
    def _validate_channel(channel):
        if not isinstance(channel, Channel):
            raise ValueError('The object is not a Channel')
        return channel

    def _start_workers(self):
        for _ in range(WORKERS):
            worker = Thread(target=self._worker, args=(self._queue,))
            worker.setDaemon(False)
            worker.start()

    def __call__(self, **kwargs):
        self.send(**kwargs)

    def send(self, **kwargs):
        """Send a message to all channels.

        Args:
            **kwargs: The arguments to send

        Returns:
            results (list): The results of the notification.

        """
        self._results = []
        for channel in self._channels:
            self._queue.put((channel, kwargs))
        self._start_workers()
        self._logger.debug('Waiting for results')
        self._queue.join()
        self._logger.debug(('Result of notification: '
                            '{result}').format(result=self._results))
        return self._results

    def _worker(self, queue):
        while not queue.empty():
            channel, kwargs = queue.get()
            self._logger.debug(('Sending notification using channel: {channel} '
                                'with args:{args}').format(channel=channel.name,
                                                           args=kwargs))
            try:
                with ThreadingTimeout(TIMEOUT):
                    result = channel.notify(**kwargs)
                    self._results.append({channel.name: result})
            except TimeoutException:
                self._logger.error(('The worker reached the time limit '
                                    '({} secs)').format(TIMEOUT))
            except Exception:  # pylint: disable=broad-except
                self._logger.exception(('Exception caught on sending on '
                                        'channel:{}').format(channel.name))
            queue.task_done()


class Notifier:
    """Model of a notifier."""

    def __init__(self):
        self._logger = logging.getLogger('{base}.{suffix}'
                                         .format(base=LOGGER_BASENAME,
                                                 suffix=self.__class__.__name__)
                                         )
        self.broadcast = Group('broadcast')

    @property
    def channels(self):
        """Channels."""
        return [channel.name for channel in self.broadcast._channels]  # noqa

    def register(self, *args):
        """Registers a channel.

        Args:
            *args: The arguments to process

        Returns:
            None

        """
        for channel in args:
            if not isinstance(channel, Channel):
                raise ValueError(('The object is not a Channel :'
                                  '[{}]').format(channel))
            if channel.name in self.channels:
                raise ValueError('Channel already registered')
            self.broadcast._channels.append(channel)  # noqa

    def unregister(self, *args):
        """Unregisters a channel.

        Args:
            *args: The arguments to process

        Returns:
            None

        """
        for channel in args:
            if channel.name not in self.channels:
                raise ValueError('Channel not registered')
            self.broadcast._channels = [ch for ch in self.broadcast._channels  # noqa
                                        if not ch.name == channel.name]

    def add_group(self, group):
        """Adds a group.

        Args:
            group: The group to add.

        Returns:
            None

        """
        if not isinstance(group, Group):
            raise ValueError(('The object is not a Group :'
                              '[{}]').format(group))
        setattr(self, group.name, group)

    def remove_group(self, group):
        """Removes a group.

        Args:
            group: The group to remove.

        Returns:
            result (bool): True on success False otherwise.

        """
        if not isinstance(group, Group):
            raise ValueError(('The object is not a Group :'
                              '[{}]').format(group))
        try:
            delattr(self, group.name)
            return True
        except AttributeError:
            self._logger.error('No such group :{}'.format(group.name))
            return False
