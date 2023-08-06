# coding=utf-8
"""
HTTP Server

Authors:
    Lazarev Ivan <lazarev.i@gmail.com>
    Dmitry Parfyonov <parfyonov.dima@gmail.com>

Copyright:
   Wakie, 2018-2021
"""

# import

from gevent.pywsgi import WSGIServer

from .errors import ErrorResponse
from .request import Request
from .response import ServerErrorResponse

# HttpServer

class HttpServer(object):

    def __init__(self, host, port, log, router, request_cls=None):
        """
        Init

        Args:
            host (str):
            port (int):
            log (logging.Logger):
            router (ghttp.router.Router):
            request_cls: (.request.Request or None):
        """
        self.__host = host
        self.__port = port
        self.__log = log
        self.__middleware = []
        self.__request_cls = request_cls or Request
        self.__router = router

    def add_middleware(self, middleware):
        """
        Add middleware

        Args:
            middleware: ghttp.middleware.Middleware
        """
        self.__middleware.append(middleware)

    def handle_request(self, env, start_response):
        """
        Handle request

        Args:
            env (dict):
            start_response (callable):

        Returns:
            str
        """
        try:
            request = self.__request_cls(env)
            try:
                for middle in self.__middleware:
                    request = middle.pre_action(request)
                response = self.__router.run_action(request)
            except ErrorResponse as e:
                response = e.get_response()

            for middle in reversed(self.__middleware):
                response = middle.post_action(request, response)
        except Exception as e:
            self.__log.error(str(e))
            response = ServerErrorResponse()

        start_response(response.get_status(), response.get_headers())
        content = response.get_content()
        if content is None:
            content = ""

        return [content.encode()]

    def serve_forever(self):
        """
        Serve forever
        """
        ls = (self.__host, self.__port)
        self.__log.debug('Listening {}:{}'.format(*ls))

        WSGIServer(
            listener=ls,
            application=self.handle_request,
            log=self.__log,
            error_log=self.__log
        ).serve_forever()
