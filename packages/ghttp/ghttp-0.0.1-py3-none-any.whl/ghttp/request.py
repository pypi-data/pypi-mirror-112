# coding=utf-8
"""
HTTP request

Authors:
    Lazarev Ivan <lazarev.i@gmail.com>
    Dmitry Parfyonov <parfyonov.dima@gmail.com>

Copyright:
   Wakie, 2018-2021
"""

# import

import json

try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl

# Request

class Request(object):

    def __init__(self, env):
        """
        Init

        Args:
            env (dict): WSGI env
        """
        self._env = env
        self._path = ''
        self._post_data = {}
        self._parse_env(env)
        self._translator = lambda x: x

    def _parse_env(self, env):
        """
        Parse env

        Args:
            env (dict):
        """
        self._path = env['PATH_INFO']
        self._query = dict(parse_qsl(env['QUERY_STRING']))
        self._content_length = int(env.get('CONTENT_LENGTH', '0'))
        self._request_method = env['REQUEST_METHOD'].lower()
        self._content_type = env.get('CONTENT_TYPE')

        self._post_data = {}
        self._raw_post = None
        if self.is_post() and self.get_content_length() > 0:
            self._raw_post = env['wsgi.input'].read(self.get_content_length())
            if self._content_type == 'application/x-www-form-urlencoded':
                self._post_data = dict(parse_qsl(self._raw_post))
            elif self._content_type == 'application/json':
                self._post_data = json.loads(self._raw_post)

        self._custom_data = {}

    def is_get(self):
        return self._request_method == 'get'

    def is_post(self):
        return self._request_method == 'post'

    def get_content_length(self):
        return self._content_length

    def get_raw_post(self):
        return self._raw_post

    def get_post_data(self):
        return self._post_data

    def get_query_data(self):
        return self._query

    def get_path(self):
        return self._path

    def get_header(self, name):
        header = 'HTTP_{}'.format(name.upper().replace('-', '_'))
        return self._env.get(header)

    def headers(self):
        """
        Get all headers

        Returns:
            dict: headers data
        """
        names = [header.replace('HTTP_', '') for header in self._env if header.startswith('HTTP_')]
        return dict([(name.replace('_', '-'), self.get_header(name)) for name in names])

    def set_custom(self, name, value):
        self._custom_data[name] = value

    def set_translator(self, t):
        self._translator = t

    def get(self, name, default=None):
        return self[name] or default

    def _(self, msg):
        return self._translator(msg)

    def __getitem__(self, item):
        if item in self._custom_data:
            return self._custom_data[item]

        if self.is_post() and item in self._post_data:
            return self._post_data[item]

        return self._query.get(item)
