from dataclasses import dataclass


@dataclass
class BasisException(Exception):
    msg: str
    code: int


@dataclass
class AppException(BasisException):
    status_code: int
