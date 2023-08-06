# coding=utf-8
"""
Errors

Authors:
    Lazarev Ivan <lazarev.i@gmail.com>
    Dmitry Parfyonov <parfyonov.dima@gmail.com>

Copyright:
   Wakie, 2018-2021
"""

# ErrorResponse

class ErrorResponse(Exception):
    def __init__(self, response):
        """
        Init

        Args:
            response (ghttp.response.Response):
        """
        self.__response = response

    def get_response(self):
        """
        Get response

        Returns:
            ghttp.response.Response
        """
        return self.__response
