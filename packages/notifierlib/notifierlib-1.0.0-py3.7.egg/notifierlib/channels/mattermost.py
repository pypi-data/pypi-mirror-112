#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: mattermost.py
"""Mattermost module file."""

import json
import requests
from jinja2 import Environment

from notifierlib.notifierlib import Channel

__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''19-09-2017'''


class Mattermost(Channel):  # pylint: disable=too-few-public-methods
    """Models a mattermost channel."""

    def __init__(self, name, webhook_url, template=None):
        super(Mattermost, self).__init__(name)
        self.url = webhook_url
        self.template = template

    def notify(self, **kwargs):
        """Notify."""
        try:
            if self.template:
                body = Environment().from_string(self.template).render(**kwargs)
            else:
                body = kwargs.get('message')
            headers = {'Content-Type': 'application/json'}
            payload = {'text': body}
            response = requests.post(self.url,
                                     data=json.dumps(payload),
                                     headers=headers,
                                     timeout=20)
            if not response.ok:
                message = (f'Error sending message to {self.url}.\n'
                           f'Message: {body}\n'
                           f'Response: '
                           f'{response.content}\n')
                self._logger.error(message)
                return False
            self._logger.debug(('Message sent successfully. Response text: '
                                '{response}').format(response=response.text))
        except Exception:  # pylint: disable=broad-except
            self._logger.exception()
            return False
        return True
