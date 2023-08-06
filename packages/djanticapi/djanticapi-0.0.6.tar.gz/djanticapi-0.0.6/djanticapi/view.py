from typing import Any, Callable, List

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied as DJPermissionDenied
from django.db import connection, transaction
from django.http import Http404, HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from pydantic.error_wrappers import ValidationError

from djanticapi import exceptions
from djanticapi.authentication import BaseAuthentication
from djanticapi.logger import logger
from djanticapi.permissions import BasePermission
from djanticapi.response import JsonResponse
from djanticapi.utils import import_object


class BaseAPIView(View):
    authentication_classes = (
        'djanticapi.authentication.SessionAuthentication',
        'djanticapi.authentication.BasicAuthentication',
        'djanticapi.jwt.authentication.JWTAuthentication',
    )
    permission_classes = ('djanticapi.permissions.AllowAny',)

    @classmethod
    def as_view(cls: Any, **initkwargs: Any) -> Callable[..., HttpResponse]:
        view = super().as_view(**initkwargs)
        return csrf_exempt(view)

    def initial(self, request: HttpRequest):
        self.check_authentication(request=request)
        self.check_permissions(request=request)

    def check_permissions(self, request: HttpRequest):
        for p in self.permissions:
            if not p.has_permission(request=request):
                raise exceptions.PermissionDeniedException(
                    err_detail=getattr(p, "err_detail", None),
                    err_code=getattr(p, "err_code", None)
                )

    def check_authentication(self, request: HttpRequest):
        session_user = getattr(request, "user", None)
        if session_user and not isinstance(session_user, AnonymousUser):
            return

        for auth in self.authenticators:
            user = auth.authenticate(request=request)
            if user is not None and not isinstance(user, AnonymousUser):
                request.user = user
                return

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            self.initial(request=request)
            result = super().dispatch(request, *args, **kwargs)
            response = self.finalize_response(result)
        except ValidationError as exc:
            logger.warning("API handler `%s` request data validation failed, reason is %s.", request.path, exc)
            exc = exceptions.FormParameterValidationException()
            response = self.handle_exception(exc)
        except Exception as exc:
            if not isinstance(exc, exceptions.BaseAPIException):
                logger.exception("API handler failed, reason is %s", exc)
            response = self.handle_exception(exc)

        return response

    def http_method_not_allowed(self, request, *args, **kwargs):
        logger.warning('Method Not Allowed (%s): %s', request.method, request.path, extra={'status_code': 405, 'request': request})
        exc = exceptions.HttpResponseNotAllowedException(err_detail='Method not allowed (%s)' % request.method)
        exc.headers = {'Allow': ', '.join(getattr(self, "_allowed_methods")())}
        raise exc

    def finalize_response(self, data: Any) -> HttpResponse:
        if isinstance(data, (JsonResponse, HttpResponse)):
            return data

        return JsonResponse(data=dict(data=data, err_msg="", err_code="Ok"))

    def handle_exception(self, exc: Exception) -> HttpResponse:
        if isinstance(exc, Http404):
            exc = exceptions.NotFoundException()
        elif isinstance(exc, DJPermissionDenied):
            exc = exceptions.PermissionDeniedException()

        if isinstance(exc, exceptions.BaseAPIException):
            result = {'err_msg': exc.err_detail, 'err_code': exc.err_code}
            http_status_code = exc.http_status_code
        else:
            result = {'err_msg': exc.__doc__, 'err_code': 'UnknownError'}
            http_status_code = 500
        # django orm transaction rollback
        self._set_django_db_rollback()
        response = JsonResponse(data=result, status=http_status_code)
        if hasattr(exc, "headers"):
            for k, v in getattr(exc, "headers", {}).items():
                response[k] = v
        return response

    @staticmethod
    def _set_django_db_rollback():
        atomic_requests = connection.settings_dict.get('ATOMIC_REQUESTS', False)
        if atomic_requests and connection.in_atomic_block:
            transaction.set_rollback(True)

    @property
    def permissions(self) -> List['BasePermission']:
        return [import_object(p)() for p in self.permission_classes]

    @property
    def authenticators(self) -> List['BaseAuthentication']:
        return [import_object(a)() for a in self.authentication_classes]
