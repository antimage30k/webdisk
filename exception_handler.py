import json
import logging

from flask import request
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


class WarningType:
    SUCCESS = 'success'
    WARNING = 'warning'
    INFO = 'info'
    ERROR = 'error'


def handle(e):
    logger.error("error info: %s" % e)  # 对错误进行日志记录
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        return e


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we made a mistake!'
    error_code = 999
    type = WarningType.ERROR

    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None, scope=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None, scope=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]


class Error:
    login_error = APIException(msg="Wrong Username or Password.")
    not_authorized = APIException(msg="Not Authorized.")
    username_occupied = APIException(msg='This username has been occupied.')
    registration_failed = APIException(msg='Registration Failed.')
    not_found = APIException(code=404, msg="Resource Not Found.")
