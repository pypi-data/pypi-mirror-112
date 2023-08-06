# coding=utf-8
"""
HTTP Server Middleware

Authors:
    Lazarev Ivan <lazarev.i@gmail.com>
    Dmitry Parfyonov <parfyonov.dima@gmail.com>

Copyright:
   Wakie, 2018-2021
"""

# import

from . import errors
from .response import UnauthorizedResponse

# Middleware

class Middleware(object):

    def pre_action(self, request):
        """
        Pre action

        Args:
            request (ghttp.request.Request):

        Returns:
            ghttp.request.Request
        """
        return request

    def post_action(self, request, response):
        """
        Post action

        Args:
            request (ghttp.request.Request):
            response (ghttp.response.Response):

        Returns:
            ghttp.response.Response
        """
        return response

# Authorization

class Authorization(Middleware):

    def __init__(self, token_to_user_func):
        """
        Init

        Args:
            token_to_user_func (callable): get user by token function
        """
        self.__token_to_user_func = token_to_user_func

    def pre_action(self, request):
        """
        Post action

        Args:
            request (ghttp.request.Request):

        Returns:
            ghttp.request.Request
        """
        token = request.get_header('X-AUTH-TOKEN')
        if not token:
            request.set_custom('is_authorized', False)
            return request

        try:
            user = self.__token_to_user_func(token)
            request.set_custom('is_authorized', True)
            request.set_custom('user', user)
        except Exception:
            request.set_custom('user', None)
            request.set_custom('is_authorized', False)
        return request

# Localization

class Localization(Middleware):

    def __init__(self, user_to_translator_func):
        """
        Init

        Args:
            user_to_translator_func (callable):
        """
        self.__user_to_translator_func = user_to_translator_func

    def pre_action(self, request):
        """
        Pre action

        Args:
            request (ghttp.request.Request):

        Returns:
            ghttp.request.Request
        """
        if request['is_authorized']:
            request.set_translator(self.__user_to_translator_func(request['user']))

        return request

# AuthorizationRequired

class AuthorizationRequired(Middleware):

    def pre_action(self, request):
        """
        Pre action

        Args:
            request (ghttp.request.Request):

        Returns:
            ghttp.request.Request
        """
        if not request['is_authorized']:
            raise errors.ErrorResponse(UnauthorizedResponse())

        return request
