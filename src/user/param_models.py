from basis.param_models import BasisModel


class Signup(BasisModel):
    email: str
    password: str
    invite_code: str


class Login(BasisModel):
    email: str
    password: str


class FillProfile(BasisModel):
    personal_id: str
    phone: str
