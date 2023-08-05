#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: slack.py
"""Slack module file."""

import requests
from jinja2 import Environment

from notifierlib.notifierlib import Channel

__author__ = '''Oriol Fabregas <fabregas.oriol@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''20-09-2017'''


class AuthenticationError(Exception):
    """If the response from the server is not successful in getting user id."""


class Slack(Channel):  # pylint: disable=too-few-public-methods
    """Integration with Slack.

    In a team, a channel is public by design, therefore the attribute 'private'
    is False by default. A private channel is just a group.

    Slack API understands a channel name as "#channel" format and a group as
    "group". Also, by default will reply to the whole channel.

    "as_user" is also implemented by default in this notification.

    +info https://api.slack.com/methods/chat.postMessage#channels
    """

    def __init__(self,  # pylint: disable=too-many-arguments
                 name,
                 token,
                 channel,
                 template=None,
                 private=False,
                 reply_broadcast=False):
        super(Slack, self).__init__(name)
        self.private = private
        self.channel = channel if self.private else '#{}'.format(channel)
        self.template = template
        self.site = 'https://slack.com/api'
        self.reply_broadcast = reply_broadcast
        self.__token = token

    def _get_user_id(self):
        url = '{site}/auth.test'.format(site=self.site)
        response = requests.post(url, data={'token': self.__token})
        if not response.json().get('ok'):
            message = ('Error getting user details from {url}.\n'
                       'Response: {res}\n').format(url=response.url,
                                                   res=response.content)
            self._logger.error(message)
            raise AuthenticationError
        return response.json().get('user_id')

    def notify(self, **kwargs):
        """Notify."""
        try:
            if self.template:
                body = Environment().from_string(self.template).render(**kwargs)
            else:
                body = kwargs.get('message')
            arguments = {'channel': self.channel,
                         'token': self.__token,
                         'text': body,
                         'reply_broadcast': self.reply_broadcast,
                         'as_user': self._get_user_id()}
            url = '{site}/chat.postMessage'.format(site=self.site)
            response = requests.post(url, data=arguments)
            if not response.json().get('ok'):
                message = ('Error while sending message to channel {} \n'
                           'Response text: {}').format(self.channel,
                                                       response.content)
                self._logger.error(message)
                result = False
            else:
                self._logger.debug('Message sent successfully.')
                result = True
        except Exception:  # pylint: disable=broad-except
            self._logger.exception()
            return False
        return result
