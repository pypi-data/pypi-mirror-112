import calendar
import datetime
import uuid
from typing import Any, Callable, Dict, Optional, Union

import jwt as PYJWT
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from django.utils.encoding import smart_bytes, smart_str
from pydantic import BaseModel

from djanticapi.authentication import BaseAuthentication
from djanticapi.exceptions import AuthenticationFailedException
from djanticapi.utils import get_username_field, import_object


class JWTAuthentication(BaseAuthentication):
    """
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string specified in the setting
    `AUTH_HEADER_PREFIX`. For example:

        Authorization: JWT eyJhbGciOiAiSFMyNTYiLCAidHlwIj
    """
    AUTH_HEADER_PREFIX = b'jwt'

    def authenticate(self, request: HttpRequest) -> Optional["AbstractBaseUser"]:
        token = self.get_token_value(request=request)
        if token is None:
            return None
        try:
            payload = jwt_config.decode_handler(token)
        except PYJWT.ExpiredSignatureError:
            raise AuthenticationFailedException('Signature has expired.')
        except PYJWT.DecodeError:
            raise AuthenticationFailedException('Error decoding signature.')
        except PYJWT.InvalidTokenError:
            raise AuthenticationFailedException('Invalid token.')

        return self.authenticate_credentials(payload=payload)

    def authenticate_credentials(self, payload: Dict[str, Any]) -> AbstractBaseUser:
        username = jwt_config.get_username_from_payload_handler(payload)
        if not username:
            raise AuthenticationFailedException('Invalid payload.')

        user = get_user_model().objects.filter(**{get_username_field(): username}).first()
        if user is None:
            raise AuthenticationFailedException('Invalid signature.')

        if not user.is_active:
            raise AuthenticationFailedException('User account is disabled.')

        return user

    def get_token_value(self, request: HttpRequest) -> Union[str, bytes, None]:
        auth_groups = self.get_auth_header(request=request).split()
        if not auth_groups:
            if jwt_config.auth_cookie_key:
                return request.COOKIES.get(jwt_config.auth_cookie_key, None)
            return None

        auth_header_prefix = jwt_config.auth_header_prefix
        if not auth_header_prefix:
            auth_header_prefix = self.AUTH_HEADER_PREFIX

        if auth_groups[0].lower() != smart_bytes(auth_header_prefix).lower():
            return None

        if len(auth_groups) == 1:
            raise AuthenticationFailedException('Invalid Authorization header. No credentials provided.')
        elif len(auth_groups) > 2:
            raise AuthenticationFailedException('Invalid Authorization header. Credentials string should not contain spaces.')

        return auth_groups[1]


def get_username_from_payload(payload: Dict[str, Any]) -> Union[str, bytes]:
    return payload.get("username", "")


def get_userid_from_payload(payload: Dict[str, Any]) -> Any:
    return payload.get("user_id")


def encode(payload: Dict[str, Any]) -> str:
    secret_key = jwt_config.private_key
    if not secret_key:
        secret_key = get_secret_key(payload=payload)

    return smart_str(PYJWT.encode(payload=payload, key=secret_key, algorithm=jwt_config.algorithm))


def decode(token: Union[str, bytes]) -> Dict[str, Any]:
    secret_key = jwt_config.public_key
    if not secret_key:
        unverified_payload = PYJWT.decode(jwt=token, key='', verify=False, options={'verify_signature': False})
        secret_key = get_secret_key(payload=unverified_payload)

    return PYJWT.decode(
        jwt=token,
        key=secret_key,
        verify=jwt_config.verify,
        options={'verify_exp': jwt_config.verify_expiration},
        leeway=jwt_config.leeway,
        audience=jwt_config.audience,
        issuer=jwt_config.issuer,
        algorithms=[jwt_config.algorithm]
    )


def get_secret_key(payload: Dict[str, Any]) -> str:
    user_secret_key_func = jwt_config.user_secret_key_handler
    if user_secret_key_func:
        user = get_user_model().objects.filter(pk=jwt_config.get_userid_from_payload_handler(payload)).first()
        secret_key = str(user_secret_key_func(user))
    else:
        secret_key = jwt_config.secret_key

    return secret_key


def payload_handler(user: AbstractBaseUser) -> Dict[str, Any]:
    payload = {
        "user_id": user.pk if not isinstance(user.pk, uuid.UUID) else str(user.pk),
        "username": user.get_username(),
        "exp": datetime.datetime.utcnow() + jwt_config.expiration_delta
    }
    email_field_name = user.get_email_field_name()
    if getattr(user, email_field_name, ""):
        payload["email"] = getattr(user, email_field_name, "")

    if jwt_config.allow_refresh:
        payload["orig_iat"] = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

    if jwt_config.audience is not None:
        payload["aud"] = jwt_config.audience

    if jwt_config.issuer is not None:
        payload["iss"] = jwt_config.issuer

    return payload


def response_payload_handler(token: str, user: AbstractBaseUser = None, request: HttpRequest = None) -> Dict[str, str]:
    return {"token": token}


DEFAULT_HANDLERS = {
    "encode_handler":  "djanticapi.jwt.authentication.encode",
    "decode_handler": "djanticapi.jwt.authentication.decode",
    "payload_handler": "djanticapi.jwt.authentication.payload_handler",
    "get_userid_from_payload_handler": "djanticapi.jwt.authentication.get_userid_from_payload",
    "get_username_from_payload_handler": "djanticapi.jwt.authentication.get_username_from_payload",
    "response_payload_handler": "djanticapi.jwt.authentication.response_payload_handler",
    "user_secret_key_handler": None
}


class JWTConfig(BaseModel):
    encode_handler: Callable[[Dict[str, Any]], str]
    decode_handler: Callable[[Union[str, bytes]], Dict[str, Any]]
    payload_handler: Callable[['AbstractBaseUser'], Dict[str, Any]]
    get_userid_from_payload_handler: Callable[[Dict[str, Any]], Union[str, bytes, int]]
    get_username_from_payload_handler: Callable[[Dict[str, Any]], Union[str, bytes]]
    response_payload_handler: Callable[[str, Optional['AbstractBaseUser'], Optional['HttpRequest']], Dict[str, Any]]
    private_key: Optional[str] = None
    public_key:  Optional[str] = None
    secret_key: str = settings.SECRET_KEY
    user_secret_key_handler: Optional[Callable[[Optional['AbstractBaseUser']], str]] = None
    algorithm: str = "HS256"
    verify: bool = True
    verify_expiration: bool = True
    leeway: int = 0
    expiration_delta: datetime.timedelta = datetime.timedelta(seconds=300)
    audience: Optional[str] = None
    issuer: Optional[str] = None
    allow_refresh: bool = True
    refresh_expiration_delta: datetime.timedelta = datetime.timedelta(days=7)
    auth_header_prefix: bytes = b'jwt'
    auth_cookie_key: Optional[str] = None

    def __init__(self, **data):
        for k, dv in DEFAULT_HANDLERS.items():
            if k not in data or not data[k]:
                v = dv
            else:
                v = data[k]
            data[k] = import_object(v)
        super().__init__(**data)


jwt_config = JWTConfig(**getattr(settings, "DJANTICAPI_AUTHENTICATION_CONFIG", {}).get("JWT", {}))
