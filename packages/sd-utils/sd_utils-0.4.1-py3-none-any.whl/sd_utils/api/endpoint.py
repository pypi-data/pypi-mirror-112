from typing import Any, Dict, List, Optional, Tuple, Union
import requests


class _Param:
    def __init__(self, expected_type, required, default_value):
        self.expected_type = expected_type
        self.required = required
        self.default_value = default_value


class QueryParam(_Param):
    pass


class BodyParam(_Param):
    pass


class Callback:
    def __init__(self, url: str, send_fn=None):
        self.__url = url
        if send_fn is None:

            def default_func(u, x):
                requests.post(u, data=x)

            self.__send_fn = default_func
        else:
            self.__send_fn = send_fn

    def __call__(self, response: Tuple[int, dict]) -> Any:
        self.__send_fn(self.__url, response)


class Endpoint:
    def __init__(
        self,
        handle_fn=None,
        params: Optional[Dict[str, Union[QueryParam, BodyParam]]] = None,
        callbacks: Optional[List[Callback]] = None,
    ):
        if handle_fn is None:

            def default_func(request):
                return (500, {"message": "Not Implemented"})

            self.__handle_fn = default_func
        else:
            self.__handle_fn = handle_fn
        self.__params = {} if params is None else params
        self.__callbacks = [] if callbacks is None else callbacks

    @staticmethod
    def __validate_input(name, meta, source):
        """
        """
        if name not in source:
            if meta.required:
                raise ValueError(
                    f'Expected parameter [{name}] not found in request {"body" if isinstance(meta, BodyParam) else "query string"}'
                )
            else:
                return meta.default_value
        if not isinstance(source[name], meta.expected_type):
            raise ValueError(
                f"Unexpected type [{type(source[name])}] found instead of [{meta.expected_type}]"
            )

        return source[name]

    def handle(self, inputs: dict) -> Tuple[int, dict]:
        return self.__handle_fn(inputs)

    def get_inputs(self, request):
        response = {}
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, BodyParam):
                response[k] = Endpoint.__validate_input(k, v, request.form)
            if isinstance(v, QueryParam):
                response[k] = Endpoint.__validate_input(k, v, request.args)
        for k, v in self.__params.items():
            if isinstance(v, BodyParam):
                response[k] = Endpoint.__validate_input(k, v, request.form)
            if isinstance(v, QueryParam):
                response[k] = Endpoint.__validate_input(k, v, request.args)
        return response

    def send_callbacks(self, response):
        for _, v in self.__dict__.items():
            if isinstance(v, Callback):
                v(response)

        for v in self.__callbacks:
            v(response)
