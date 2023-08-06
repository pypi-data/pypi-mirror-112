import base64
import binascii
from typing import Any, Optional

from django.contrib.auth import authenticate
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import CsrfViewMiddleware
from django.utils.encoding import DjangoUnicodeDecodeError, smart_bytes, smart_str

from djanticapi.exceptions import (
    AuthenticationFailedException,
    PermissionDeniedException,
)
from djanticapi.utils import get_username_field


class BaseAuthentication:
    AUTH_HEADER_PREFIX = b""

    def authenticate(self, request: HttpRequest) -> Optional["AbstractBaseUser"]:
        raise NotImplementedError(".authenticate() must be overridden.")

    def get_auth_header(self, request: HttpRequest) -> bytes:
        auth = request.META.get("HTTP_AUTHORIZATION", b'')
        return smart_bytes(auth)


class BasicAuthentication(BaseAuthentication):
    """
    HTTP Basic authentication against username/password.
    """
    AUTH_HEADER_PREFIX = b'basic'

    def authenticate(self, request: HttpRequest) -> Optional["AbstractBaseUser"]:
        auth_groups = self.get_auth_header(request=request).split()
        if not auth_groups or auth_groups[0].lower() != self.AUTH_HEADER_PREFIX:
            return None
        if len(auth_groups) == 1:
            raise AuthenticationFailedException('Invalid basic header. No credentials provided.')
        elif len(auth_groups) > 2:
            raise AuthenticationFailedException('Invalid basic header. Credentials string should not contain spaces.')

        try:
            auth_decoded = smart_str(base64.b64decode(auth_groups[1]))
        except (TypeError, DjangoUnicodeDecodeError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationFailedException('Invalid basic header. Credentials not correctly base64 encoded.')

        auth_parts = auth_decoded.partition(':')
        username, password = auth_parts[0], auth_parts[2]

        return self.authenticate_credentials(username, password, request)

    def authenticate_credentials(self, username: Any, password: Any, request: HttpRequest = None) -> AbstractBaseUser:
        credentials = {get_username_field(): username, 'password': password}
        user = authenticate(request=request, **credentials)
        if user is None:
            raise AuthenticationFailedException('Invalid username/password.')
        if not user.is_active:
            raise AuthenticationFailedException('User inactive or deleted.')

        return user


class _csrf_check(CsrfViewMiddleware):
    def _reject(self, request: HttpRequest, reason: Any):
        # Return the failure reason instead of an HttpResponse
        return reason


class SessionAuthentication(BaseAuthentication):
    """
    Use Django's session framework for authentication.
    """

    def authenticate(self, request: HttpRequest) -> Optional["AbstractBaseUser"]:
        user = getattr(request, 'user', None)
        if not user or not user.is_active:
            return None
        self.enforce_csrf(request)
        return user

    @staticmethod
    def _dummy_get_response(request: HttpRequest) -> 'HttpResponse':
        return HttpResponse()

    def enforce_csrf(self, request: HttpRequest):
        check = _csrf_check(get_response=self._dummy_get_response)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        # CSRF failed, bail with explicit error message
        if reason:
            raise PermissionDeniedException('CSRF Failed: %s' % reason)
