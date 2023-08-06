from typing import Any, Optional


class Field:
    SLUG = "__field_"

    def __init__(
        self,
        expected_type=Any,
        required: bool = False,
        default_value: Optional[Any] = None,
    ):
        self.expected_type = expected_type
        self.required = required
        self.default_value = default_value

    def __set_name__(self, owner, name):
        self.private_name = Field.SLUG + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    def validate(self, value):
        if not self.required and value is None:
            return
        if not isinstance(value, self.expected_type):
            raise ValueError(
                f"Expected type of {self.private_name[len(Field.SLUG):]} to be [{self.expected_type!r}] not [{type(value)!r}]"
            )
