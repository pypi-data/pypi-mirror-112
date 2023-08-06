from abc import ABC
from typing import Callable, Optional


class Error(ABC):
    SLUG = "__api_error_"

    def __init__(
        self,
        code: int,
        message: str,
        error_func: Optional[Callable[[int, dict], bool]] = None,
    ):
        self._code = code
        self._message = message
        self.error_func = (
            error_func
            if error_func is not None
            else lambda status_code, content: status_code == self._code
        )

    def __set_name__(self, owner, name):
        self.private_name = Error.SLUG + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        setattr(obj, self.private_name, value)

    def _set_api_name(self, name):
        self._api_name = name

    def _is_error(self, status_code: int, content: dict):
        return self.error_func(status_code, content)

    @property
    def code(self) -> int:
        return self._code

    @property
    def message(self) -> str:
        return self._message
