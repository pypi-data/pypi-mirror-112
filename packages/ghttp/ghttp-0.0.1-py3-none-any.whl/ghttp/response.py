# coding=utf-8
"""
HTTP response

Authors:
    Lazarev Ivan <lazarev.i@gmail.com>
    Dmitry Parfyonov <parfyonov.dima@gmail.com>

Copyright:
   Wakie, 2018-2021
"""

# import

import json

# Response

class Response(object):

    def __init__(self, content='', headers=None):
        """
        Init

        Args:
            content (mixed):
            headers (list[tuple] or None): headers [("<header_name>", "<header_value>"), ...]
        """
        self._status = '200 OK'
        self._content_type = 'text/plain'
        self._content = content
        self._headers = headers or []

    def get_status(self):
        """
        Get status

        Returns:
            str
        """
        return self._status

    def add_heades(self, headers):
        """
        Add headers

        Args:
            headers (list[tuple]): headers [("<header_name>", "<header_value>"), ...]
        """
        self._headers += headers

    def get_headers(self):
        """
        Get headers

        Returns:
            list[tuple]: headers [("<header_name>", "<header_value>"), ...]
        """
        return [('Content-type', self._content_type)] + self._headers

    def get_content(self):
        """
        Get content

        Returns:
            str
        """
        return self._content

# ServerErrorResponse

class ServerErrorResponse(Response):

    def __init__(self, content=None, headers=None):
        """
        Init

        Args:
            content (mixed):
            headers (list[tuple] or None): headers [("<header_name>", "<header_value>"), ...]
        """
        super(ServerErrorResponse, self).__init__(content, headers)
        self._status = '500 Server Error'

# NotFoundResponse

class NotFoundResponse(Response):

    def __init__(self, content=None, headers=None):
        """
        Init

        Args:
            content (mixed):
            headers (list[tuple] or None): headers [("<header_name>", "<header_value>"), ...]
        """
        super(NotFoundResponse, self).__init__(content, headers)
        self._status = '404 Not Found'

# BadRequest

class BadRequest(Response):

    def __init__(self, field, error, message, headers=None):
        """
        Init

        Args:
            field (str):
            error (str):
            message (str):
            headers (list[tuple] or None): headers [("<header_name>", "<header_value>"), ...]
        """
        content = dict(error=u"{}_{}".format(field, error), message=message)
        super(BadRequest, self).__init__(content, headers)
        self._status = '400 Bad Request'

# UnauthorizedResponse

class UnauthorizedResponse(Response):

    def __init__(self, content=None, headers=None):
        """
        Init

        Args:
            content (mixed):
            headers (list[tuple] or None): headers [("<header_name>", "<header_value>"), ...]
        """
        super(UnauthorizedResponse, self).__init__(content, headers)
        self._status = '401 Unauthorized'

# JsonResponse

class JsonResponse(Response):

    def __init__(self, content=None, headers=None):
        """
        Init

        Args:
            content (dict or None):
            headers (list[tuple] or None): headers [("<header_name>", "<header_value>"), ...]
        """
        super(JsonResponse, self).__init__(content, headers)
        self._content_type = 'application/json'
        self._content = content

    def get_headers(self):
        """
        Get headers

        Returns:
            list[tuple]: headers [("<header_name>", "<header_value>"), ...]
        """
        headers = super(JsonResponse, self).get_headers()

        return headers + self._headers

    def get_content(self):
        """
        Get content

        Returns:
            str or unicode
        """
        return json.dumps({
            'ok': self.get_status() == '200 OK',
            'content': self._content or {}
        })

# JsonNotFoundResponse

class JsonNotFoundResponse(JsonResponse):

    def __init__(self, content=None, headers=None):
        """
        Init

        Args:
            content (dict or None):
            headers (list[tuple] or None): headers [("<header_name>", "<header_value>"), ...]
        """
        super(JsonNotFoundResponse, self).__init__(content, headers)
        self._status = '404 Not Found'

# JsonBadRequest

class JsonBadRequest(JsonResponse):

    def __init__(self, field, error, message, headers=None):
        """
        Init

        Args:
            field (str):
            error (str):
            message (str):
            headers (list[tuple] or None): headers [("<header_name>", "<header_value>"), ...]
        """
        content = dict(error=u"{}_{}".format(field, error), message=message)
        super(JsonBadRequest, self).__init__(content, headers)
        self._status = '400 Bad Request'

# JsonUnauthorizedResponse

class JsonUnauthorizedResponse(JsonResponse):

    def __init__(self, content=None, headers=None):
        """
        Init

        Args:
            content (dict or None):
            headers (list[tuple] or None): headers [("<header_name>", "<header_value>"), ...]
        """
        super(JsonUnauthorizedResponse, self).__init__(content, headers)
        self._status = '401 Unauthorized'

# JsonServerErrorResponse

class JsonServerErrorResponse(JsonResponse):

    def __init__(self, content=None, headers=None):
        """
        Init

        Args:
            content (dict or None):
            headers (list[tuple] or None): headers [("<header_name>", "<header_value>"), ...]
        """
        super(JsonServerErrorResponse, self).__init__(content, headers)
        self._status = '500 Server Error'

# HeadJsonResponse

class HeadJsonResponse(JsonResponse):

    def get_content(self):
        """
        Get content

        Returns:
            str or unicode
        """
        return ""
