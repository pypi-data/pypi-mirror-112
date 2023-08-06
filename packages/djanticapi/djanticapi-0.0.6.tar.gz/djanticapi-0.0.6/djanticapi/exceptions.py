from typing import Any, Dict


class BaseAPIException(Exception):
    http_status_code = 500
    default_err_detail = "A server error occurred."
    default_err_code = "UnknownError"
    _headers = {}

    def __init__(self, err_detail: str = None, err_code: str = None) -> None:
        self.err_detail = err_detail if err_detail is not None else self.default_err_detail
        self.err_code = err_code if err_code is not None else self.default_err_code

    @property
    def headers(self) -> Dict[str, Any]:
        return self._headers

    @headers.setter
    def headers(self, headers: Dict[str, Any]):
        self._headers = headers


class AuthenticationFailedException(BaseAPIException):
    http_status_code = 401
    default_err_detail = "Incorrect authentication credentials."
    default_err_code = "AuthenticationFailed"


class NotFoundException(BaseAPIException):
    http_status_code = 404
    default_err_detail = "Not found."
    default_err_code = "NotFound"


class PermissionDeniedException(BaseAPIException):
    http_status_code = 403
    default_err_detail = 'You do not have permission to perform this action.'
    default_err_code = 'PermissionDenied'


class FormParameterValidationException(BaseAPIException):
    http_status_code = 400
    default_err_detail = 'Illegal parameter in request parameter.'
    default_err_code = 'IllegalParameter'


class FormParseException(BaseAPIException):
    http_status_code = 400
    default_err_detail = 'Malformed request.'
    default_err_code = 'ParseError'


class UnsupportedMediaTypeException(BaseAPIException):
    http_status_code = 415
    default_err_detail = 'Unsupported media type in request.'
    default_err_code = 'UnsupportedMediaType'


class HttpResponseNotAllowedException(BaseAPIException):
    http_status_code = 405
    default_err_detail = 'Http response not allowed.'
    default_err_code = 'HttpResponseNotAllowed'


class InvalidTokenException(BaseAPIException):
    http_status_code = 401
    default_err_detail = "Incorrect token credentials."
    default_err_code = "InvalidToken"
