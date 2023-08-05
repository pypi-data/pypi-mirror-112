#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: stdout.py
"""Stdout module file."""

from notifierlib.notifierlib import Channel


__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''18-09-2017'''


class Stdout(Channel):  # pylint: disable=too-few-public-methods
    """A simple library to print to stdout."""

    @staticmethod
    def _format_arguments(arguments):
        if not arguments.keys():
            return ''
        output = []
        longer_string_length = len(max(arguments.keys(), key=len))
        keys = sorted(arguments.keys())
        for entry in keys:
            width = longer_string_length + 1 - len(entry)
            text = ' '.join([word.capitalize() for word in entry.split()])
            value = arguments[entry]
            output.append('{legend:{align}{width}} :{value}'.format(legend=text,
                                                                    align='<',
                                                                    width=width,
                                                                    value=value)
                          )
        return '\n'.join(output)

    def notify(self, **kwargs):
        """Notify."""
        try:
            print(self._format_arguments(kwargs))
        except Exception:  # pylint: disable=broad-except
            self._logger.exception()
            return False
        return True
