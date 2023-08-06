from djanticapi.form import BaseFormModel


class ObtainJWTForm(BaseFormModel):
    username: str
    password: str


class VerifyJWTForm(BaseFormModel):
    token: str
