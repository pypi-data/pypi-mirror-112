from sd_utils.api.error import Error
from typing import Optional
from requests.auth import AuthBase
from sd_utils.api.request import Request


def __inject_base_methods(cls):
    @classmethod
    def provide_auth(cls, auth: AuthBase):
        for _, v in cls.__dict__.items():
            if isinstance(v, Request):
                v.auth = auth

    setattr(cls, "provide_auth", provide_auth)

    @classmethod
    def requests(cls):
        response = {}
        for k, v in cls.__dict__.items():
            if isinstance(v, Request):
                response[k] = v
        return response

    setattr(cls, "requests", requests)

    @classmethod
    def errors(cls):
        response = {}
        for k, v in cls.__dict__.items():
            if isinstance(v, Error):
                response[k] = v
        return response

    setattr(cls, "errors", errors)


def client_api(
    base_url: str, headers: dict = {}, auth: Optional[AuthBase] = None
):
    def decorator(cls):
        errors = set()
        for k, v in cls.__dict__.items():
            if isinstance(v, Error):
                errors.add(v)
                v._set_api_name(k)
                setattr(cls, k, v)

        for k, v in cls.__dict__.items():
            if isinstance(v, Request):
                v._configure(base_url, headers, auth, errors)
                setattr(cls, k, v)

        __inject_base_methods(cls)

        return cls

    return decorator
