from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from django.conf import settings
from django.http import HttpRequest, QueryDict
from django.http.multipartparser import MultiPartParserError, parse_header
from django.utils.datastructures import MultiValueDict
from pydantic import BaseModel

from djanticapi import json
from djanticapi.exceptions import FormParseException, UnsupportedMediaTypeException


TBaseFormModel = TypeVar("TBaseFormModel", bound="BaseFormModel")


def valuedict_to_json(valuedict: MultiValueDict) -> Dict[str, Any]:
    full_data = {}
    for k in valuedict:
        v = valuedict.getlist(k, [None])
        if len(v) == 1:
            v = v[-1]
        full_data[k] = v
    return full_data


class BaseParser:
    content_type = ''

    def parse(self,  request: HttpRequest) -> Tuple[Union[MultiValueDict, Dict], Optional[MultiValueDict]]:
        "returns a tuple of ``(MultiValueDict(Request Data), MultiValueDict(FILES))`"
        raise NotImplementedError(".parse() must be overridden.")


class JSONParser(BaseParser):
    content_type = 'application/json'

    def parse(self, request: HttpRequest) -> Tuple[Union[MultiValueDict, Dict], Optional[MultiValueDict]]:
        try:
            return json.loads(request.body), None
        except ValueError as exc:
            raise FormParseException('JSON parse error - %s' % exc)


class FormParser(BaseParser):
    content_type = 'application/x-www-form-urlencoded'

    def parse(self, request: HttpRequest) -> Tuple[Union[MultiValueDict, Dict], Optional[MultiValueDict]]:
        try:
            return QueryDict(request.body), None
        except ValueError as exc:
            raise FormParseException('Form parse error - %s' % exc)


class MultiPartParser(BaseParser):
    content_type = 'multipart/form-data'

    def parse(self, request: HttpRequest) -> Tuple[Union[MultiValueDict, Dict], Optional[MultiValueDict]]:
        try:
            post_data = request.POST
            files_data = request.FILES
            return post_data, files_data
        except MultiPartParserError as exc:
            raise FormParseException('Multipart form parse error - %s' % exc)


class ParserManager:
    def __init__(self) -> None:
        self._parsers: List["BaseParser"] = []

    def register(self, parser: 'BaseParser') -> bool:
        self._parsers.append(parser)
        return True

    def get(self, content_type: str) -> 'BaseParser':
        for p in self._parsers:
            if p.content_type in content_type:
                return p
        raise UnsupportedMediaTypeException('Unsupported media type "%s" in request.' % content_type)


parsers = ParserManager()
parsers.register(JSONParser())
parsers.register(FormParser())
parsers.register(MultiPartParser())


class BaseFormModel(BaseModel):
    @classmethod
    def from_request(cls: Type[TBaseFormModel], request: HttpRequest) -> TBaseFormModel:
        if request.method.upper() == "GET":
            query_params = valuedict_to_json(request.GET)
            return cls(**query_params)

        meta = request.META
        try:
            content_length = int(meta.get('CONTENT_LENGTH', meta.get('HTTP_CONTENT_LENGTH', 0)))
        except (ValueError, TypeError):
            content_length = 0

        if content_length == 0:
            return cls()

        content_type = meta.get('CONTENT_TYPE', meta.get('HTTP_CONTENT_TYPE', ''))
        base_content_type, _ = parse_header(content_type.encode(settings.DEFAULT_CHARSET))
        if not base_content_type:
            return cls()
        parser = parsers.get(content_type=base_content_type)
        request_data, files = parser.parse(request)
        if isinstance(request_data, MultiValueDict):
            _full_data = valuedict_to_json(request_data)
        else:
            _full_data = request_data

        if files is not None:
            if isinstance(files, MultiValueDict):
                _full_data.update(valuedict_to_json(files))
            else:
                _full_data.update(files)

        return cls(**_full_data)
