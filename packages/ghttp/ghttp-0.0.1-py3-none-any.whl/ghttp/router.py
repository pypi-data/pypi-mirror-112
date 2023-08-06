# coding=utf-8
"""
HTTP actions router

Authors:
    Lazarev Ivan <lazarev.i@gmail.com>
    Dmitry Parfyonov <parfyonov.dima@gmail.com>

Copyright:
   Wakie, 2018-2021
"""

# import

import os
from os.path import join

from .errors import ErrorResponse
from .response import NotFoundResponse

# Router

class Router(object):

    def __init__(self, log=None):
        """
        Init

        Args:
            log (logging.Logger or None):
        """
        self.__actions = {}
        self.__log = log

    def register_action(self, action_name, action):
        """
        Register action

        Args:
            action_name (str):
            action (callable):
        """
        self.__actions[action_name] = action

        if self.__log:
            self.__log.debug("Router register action {} [{}.{}]".format(
                action_name, action.__module__, action.__name__
            ))

    def autoload(self, path, base_import_path):
        """
        Autoload actions from path

        Args:
            path (str): path to actions
            base_import_path (str): base import path like "myproject.http_actions"

        Examples:
            structure:
                user/auth.py:action_auth
                user/auth.py:action_token
                user/user.py:action_update
                profile.py:action_read
            will be route as:
                /user/auth
                /user/auth/token
                /user/update
                /profile/read
        """
        for module, def_action, actions_path in self.__load_modules('', base_path=path, base_import_path=base_import_path):
            if not def_action.startswith('action_') or not callable(getattr(module, def_action)):
                continue

            action = actions_path
            module_name = module.__name__.split('.')[-1]
            if not action:
                action = module_name
            elif action != module_name and not action.endswith('.{}'.format(module_name)):
                action = "{}.{}".format(action, module_name)

            action = "/{}.{}".format(action, def_action.replace('action_', '', 1)).replace('.', '/')
            self.__actions[action] = getattr(module, def_action)
            if self.__log:
                self.__log.debug("Router autoload action {} [{}.{}]".format(
                    action, self.__actions[action].__module__, self.__actions[action].__name__
                ))

    # private load modules

    def __load_modules(self, path, base_path, base_import_path):
        """
        Load modules

        Args
            path (str): path to modules directory relative base path
            base_path (str): base path to modules directory
            base_import_path (str): base import path like "myproject.http_actions"
        Yields:
            tuple[module (module), action (function), action_path (str)]
        """
        abspath = join(base_path, path) if path else base_path
        actions_path = path.replace(os.sep, '.')

        for module_name in os.listdir(abspath):
            if os.path.isdir(os.path.join(abspath, module_name)):
                for m, da, ap in self.__load_modules(os.path.join(path, module_name), base_path, base_import_path):
                    yield m, da, ap
                continue

            if module_name == '__init__.py' or not module_name.endswith('.py'):
                continue

            module_name = module_name.replace('.py', '')
            module_path = actions_path
            module_path = "{}.{}".format(module_path, module_name) if module_path else module_name

            module = __import__('{}.{}'.format(base_import_path, module_path), globals(), locals())
            for m in base_import_path.split('.')[1:]:
                module = getattr(module, m)

            for m in module_path.split('.'):
                module = getattr(module, m)

            for def_action in dir(module):
                yield module, def_action, actions_path

    def run_action(self, request):
        """
        Run action

        Args:
            request (.request.Request):

        Returns:
            .response.Response
        """
        path = request.get_path().split('/')

        if path[0] == '':
            path = path[1:]

        action_name = '/' + '/'.join(path)
        if action_name not in self.__actions:
            raise ErrorResponse(NotFoundResponse())

        return self.__actions[action_name](request)
