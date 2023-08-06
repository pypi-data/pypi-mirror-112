import calendar
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import jwt as PYJWT
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest

from djanticapi.exceptions import AuthenticationFailedException, InvalidTokenException
from djanticapi.jwt import forms
from djanticapi.jwt.authentication import jwt_config
from djanticapi.response import JsonResponse
from djanticapi.utils import get_username_field
from djanticapi.view import BaseAPIView


class _BaseJWTAPIView(BaseAPIView):
    authentication_cls_list = ()
    permission_cls_list = ()

    def post(self, request: HttpRequest):
        user = self.get_user(request=request)
        if not user.is_active:
            raise AuthenticationFailedException('User account is disabled.')
        token = self.get_token(user)
        response_data = jwt_config.response_payload_handler(token, user, request)
        response = JsonResponse(response_data)
        if jwt_config.auth_cookie_key:
            exp = datetime.utcnow()+jwt_config.expiration_delta
            response.set_cookie(jwt_config.auth_cookie_key, token, expires=exp, httponly=True)

        return response

    def get_user(self, request: HttpRequest) -> AbstractBaseUser:
        raise NotImplementedError()

    def get_token(self, user: AbstractBaseUser) -> str:
        payload = jwt_config.payload_handler(user)
        token = jwt_config.encode_handler(payload)
        return token


class ObtainJWTAPIView(_BaseJWTAPIView):
    def get_user(self, request: HttpRequest) -> AbstractBaseUser:
        form_data = forms.ObtainJWTForm.from_request(request=request)
        user = authenticate(**{get_username_field(): form_data.username, "password": form_data.password})
        if not user:
            raise AuthenticationFailedException('Unable to log in with provided credentials.')

        return user


class VerifyJWTAPIView(_BaseJWTAPIView):
    _token: str

    def get_payload(self) -> Dict[str, Any]:
        try:
            payload = jwt_config.decode_handler(self._token)
        except PYJWT.ExpiredSignatureError:
            raise InvalidTokenException('Signature has expired.')
        except PYJWT.DecodeError:
            raise InvalidTokenException('Error decoding signature.')
        except PYJWT.InvalidTokenError:
            raise InvalidTokenException('Invalid token.')

        return payload

    def get_user(self, request: HttpRequest) -> Optional["AbstractBaseUser"]:
        form_data = forms.VerifyJWTForm.from_request(request=request)
        self._token = form_data.token
        payload = self.get_payload()
        username = jwt_config.get_username_from_payload_handler(payload)
        if not username:
            raise AuthenticationFailedException('Invalid payload.')

        user = get_user_model().objects.filter(**{get_username_field(): username}).first()
        if user is None:
            raise AuthenticationFailedException('Invalid signature.')

        return user

    def get_token(self, user: AbstractBaseUser) -> str:
        return self._token


class RefreshJWTAPIView(VerifyJWTAPIView):
    _orig_iat: int

    def get_payload(self) -> Dict[str, Any]:
        payload = super().get_payload()
        orig_iat = payload.get("orig_iat")
        if not orig_iat:
            raise InvalidTokenException("Invalid payload, the reason may be that orig_iat field is required.")
        refresh_delta = jwt_config.refresh_expiration_delta
        if isinstance(refresh_delta, timedelta):
            refresh_timestamp = refresh_delta.days * 24 * 3600 + refresh_delta.seconds
        else:
            refresh_timestamp = refresh_delta

        self._orig_iat = int(orig_iat)
        exp_timestamp = self._orig_iat + int(refresh_timestamp)
        now_timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
        if now_timestamp > exp_timestamp:
            raise InvalidTokenException('Refresh has expired.')

        return payload

    def get_token(self, user: AbstractBaseUser) -> str:
        payload = jwt_config.payload_handler(user)
        payload["orig_iat"] = self._orig_iat
        token = jwt_config.encode_handler(payload)
        return token


obtain_jwt_view = ObtainJWTAPIView.as_view()
verify_jwt_view = VerifyJWTAPIView.as_view()
refresh_jwt_view = RefreshJWTAPIView.as_view()
