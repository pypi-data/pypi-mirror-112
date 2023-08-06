from typing import Any, Callable

from django.http import HttpResponse

from djanticapi import json


class JsonResponse(HttpResponse):
    def __init__(self, data, encoder: Callable[[Any], Any] = None, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        data = json.dumps(data, default=encoder)
        super().__init__(content=data, **kwargs)
