import re
from typing import Callable, Iterable
from flask import Flask, Response, request

# Yet Another Flask CORS Extension
# --------------------------------
# Based on https://developer.mozilla.org/de/docs/Web/HTTP/CORS

# DEFAULT_CONFIGURATION = {
#     'origins': '*',
#     'allowed_methods': ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE'],
#     'allowed_headers': '*',
#     'allow_credentials': True,
#     'cache_max_age': str(60 * 5)
# }

DEFAULT_CONFIGURATION = {
    'origins': None,
    'allowed_methods': [],
    'allowed_headers': None,
    'allow_credentials': False,
    'cache_max_age': None
}


class Yafcorse(object):
    def __init__(self, configuration: dict = DEFAULT_CONFIGURATION, app: Flask = None) -> None:
        super().__init__()
        self.__initialized = False

        self.__origins = configuration.get('origins', DEFAULT_CONFIGURATION.get('origins'))
        self.__regex_origin_patterns = configuration.get('origin_patterns', None)
        self.__allowed_methods = configuration.get('allowed_methods', DEFAULT_CONFIGURATION.get('allowed_methods'))
        self.__allowed_headers = configuration.get('allowed_headers', DEFAULT_CONFIGURATION.get('allowed_headers'))
        self.__allow_credentials = configuration.get('allow_credentials', DEFAULT_CONFIGURATION.get('allow_credentials'))
        self.__max_age = configuration.get('cache_max_age', DEFAULT_CONFIGURATION.get('cache_max_age'))

        self.__allowed_methods_value = ''
        self.__allowed_headers_value = ''

        self.init_app(app)

    def init_app(self, app: Flask):
        if not self.__initialized and app:
            
            self.__allowed_methods_value = ', '.join(self.__allowed_methods)
            self.__allowed_methods = [m.strip().lower() for m in self.__allowed_methods]
            self.__allowed_headers_value = ', '.join(self.__allowed_headers)
            self.__allowed_headers = [h.strip().lower() for h in self.__allowed_headers]

            if not isinstance(self.__origins, str) and isinstance(self.__origins, (list, tuple, Iterable)):
                self.__validate_origin = _check_if_contains_origin(self.__origins)
            elif isinstance(self.__origins, Callable):
                self.__validate_origin = self.__origins
            elif self.__regex_origin_patterns is not None:
                self.__validate_origin = _check_if_regex_match_origin(self.__regex_origin_patterns)
            else:
                self.__validate_origin = _check_if_asterisk_origin(self.__origins)

            app.after_request(self.__handle_response)

            app.extensions['yafcorse'] = self
            self.__initialized = True

    def __append_headers(self, response: Response, origin: str, is_preflight_request: bool = False):
        response.headers.add_header('Access-Control-Allow-Origin', origin)

        if 'Access-Control-Request-Method' in request.headers \
            and request.headers.get('Access-Control-Request-Method', '').strip().lower() in self.__allowed_methods:
            response.headers.add_header('Access-Control-Allow-Methods', self.__allowed_methods_value)

        if 'Access-Control-Request-Headers' in request.headers \
            and _string_list_in(request.headers.get('Access-Control-Request-Headers').split(','), self.__allowed_headers):
            response.headers.add_header('Access-Control-Allow-Headers', self.__allowed_headers_value)

        if self.__allow_credentials:
            response.headers.add_header('Access-Control-Allow-Credentials', 'true')
        if is_preflight_request:
            response.headers.add_header('Access-Control-Max-Age', self.__max_age)

    def __handle_response(self, response: Response):
        is_preflight_request = request.method == 'OPTIONS'
        if not is_preflight_request and 'Origin' not in request.headers:
            return response

        origin = request.headers.get('Origin')

        if not self.__validate_origin(origin):
            return response

        self.__append_headers(response, origin, is_preflight_request)
        return response


def _string_list_in(target: list[str], source: list[str]):
   contained = [element for element in target if element.strip().lower() in source]
   return contained == target


def _check_if_regex_match_origin(patterns):
    compiled_patterns = [re.compile(p) for p in patterns]
    def execute_check(origin):
        for matcher in compiled_patterns:
            if matcher.match(origin):
                return True
        return False

    execute_check.__name__ = _check_if_regex_match_origin.__name__
    return execute_check


def _check_if_contains_origin(origins):
    def execute_check(origin):
        for o in origins:
            if o == origin:
                return True
        return False

    execute_check.__name__ = _check_if_contains_origin.__name__
    return execute_check


def _check_if_asterisk_origin(origins):
    allow_all = origins == '*'
    def execute_check(origin):
        return allow_all and origin is not None

    execute_check.__name__ = _check_if_asterisk_origin.__name__
    return execute_check
