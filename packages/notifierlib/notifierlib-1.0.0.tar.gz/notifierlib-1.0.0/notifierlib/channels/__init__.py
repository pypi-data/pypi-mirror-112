#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: __init__.py
"""channels package."""

from .email import Email
from .stdout import Stdout
from .jabber import Jabber, JabberGroup
from .mattermost import Mattermost
from .telegram_ import Telegram
from .slack import Slack


__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''18-09-2017'''

# assert modules
assert Email
assert Stdout
assert Jabber
assert JabberGroup
assert Mattermost
assert Telegram
assert Slack
