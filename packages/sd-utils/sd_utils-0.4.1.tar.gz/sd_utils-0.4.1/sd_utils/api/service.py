from sd_utils.api.provider import HttpProvider
from sd_utils.api.endpoint import Endpoint


def service(http_provider: HttpProvider):
    def decorator(cls):
        for k, v in cls.__dict__.items():
            if isinstance(v, Endpoint):
                url = f"/{k.replace('_', '/')}"
                http_provider.add_endpoint(url, "GET", v)
                setattr(cls, k, v)
        return cls

    return decorator
