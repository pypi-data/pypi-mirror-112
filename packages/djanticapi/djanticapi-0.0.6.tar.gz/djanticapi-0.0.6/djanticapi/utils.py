from typing import Any

from django.utils.module_loading import import_string
from django.contrib.auth import get_user_model


def import_object(dotted_path: str) -> Any:
    if not isinstance(dotted_path, (str, bytes)):
        return dotted_path
    if isinstance(dotted_path, bytes):
        dotted_path = dotted_path.decode("utf-8")
    if dotted_path.count(".") == 0:
        return __import__(dotted_path)

    return import_string(dotted_path)


def get_username_field() -> str:
    return getattr(get_user_model(), "USERNAME_FIELD", "username")
