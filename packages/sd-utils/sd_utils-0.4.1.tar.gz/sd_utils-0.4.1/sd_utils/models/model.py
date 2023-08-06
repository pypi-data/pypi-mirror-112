from typing import Dict
from sd_utils.models.field import Field


class Model:
    @staticmethod
    def __init_method(obj, attrs: Dict[str, Field], *args, **kwargs):
        # Skimping on the argument-checking because I'm lazy.
        if len(args) > 0:
            raise TypeError("positional arguments not supported yet")

        provided = set()

        for attr, val in zip(attrs.keys(), args):
            setattr(obj, attr, val)
            provided.add(attr)
        for attr, val in kwargs.items():
            if attr not in attrs and attr != "None":
                raise TypeError(f"got an unexpected keyword argument {attr!r}")
            provided.add(attr)
            setattr(obj, attr, val)

        for attr, v in attrs.items():
            if attr not in provided:
                print(attr + " " + str(v.default_value))
                setattr(obj, attr, v.default_value)

    def __init_subclass__(cls, base_field: Field = Field, **kwargs) -> None:
        super().__init_subclass__()
        attrs: Dict[str, base_field] = {}
        for k, v in cls.__dict__.items():
            if isinstance(v, base_field):
                attrs[k] = v

        def __init__(self, *args, **kwargs):
            Model.__init_method(self, attrs, *args, **kwargs)

        cls.__init__ = __init__
        if kwargs.get("repr", True):
            repr_format = (
                "<" + ", ".join(f"{attr}={{{attr}!r}}" for attr in attrs) + ">"
            )

            def __repr__(self):
                all_attrs = self.__class__.__dict__.copy()
                all_attrs.update(self.__dict__)
                return repr_format.format_map(all_attrs)

            cls.__repr__ = __repr__
