## Requirements

Python 3.6+

Djanticapi stands on the shoulders of giants:

* <a href="https://docs.djangoproject.com/en/3.0/" class="external-link" target="_blank">Django</a> for the web parts.
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a> for the data parts.

## Installation

<div class="termy">

```console
$ pip install djanticapi

---> 100%
```

</div>

## Example

### Create it

* Create a file `api.py` with:

```Python
from django.http import HttpRequest
from djanticapi import BaseFormModel, BaseAPIView

class TestForm(BaseFormModel):
    name: str


class TestView(BaseAPIView):
    def post(self, request: HttpRequest):
        form_data = TestForm.from_request(request=request)
        return form_data
```
