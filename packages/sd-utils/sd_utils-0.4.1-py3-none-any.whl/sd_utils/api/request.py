from requests.models import Response
from sd_utils.api.error import Error
from typing import Any, Optional, Set, Union
from abc import ABC, abstractmethod
import requests

from requests.auth import AuthBase


class Request(ABC):
    def __init__(
        self,
        endpoint: str,
        body: dict = {},
        auth: Union[AuthBase, None] = None,
        documentation: str = "",
    ):
        self.endpoint = endpoint
        self.body = body
        self.auth = auth
        self._documentation = documentation

    @property
    def documentation(self) -> str:
        return self._documentation

    def __call__(self, query: str = "", body: dict = {}) -> Any:
        return self._make_request(query, body)

    @abstractmethod
    def _make_request(
        self,
        method: str,
        query: str = "",
        body: dict = {},
        headers: dict = {},
        auth: Optional[AuthBase] = None,
    ) -> Any:
        if not self.endpoint.startswith("/"):
            self.endpoint = "/" + self.endpoint
        url = f"{self.base_url}{self.endpoint}"
        if query != "":
            if not query.startswith("/"):
                query = "/" + query
            url += f"{query}"

        data = self.body
        if body != {}:
            data = {**data, **body}

        header_data = self.headers
        if headers != {}:
            header_data = {**header_data, **headers}

        auth_data = self.auth
        if auth is not None:
            auth_data = auth

        response: Response = requests.request(
            method, url, data=data, headers=header_data, auth=auth_data
        )

        if response.status_code != 200:  # basic definition of errors
            self.__handle_error(response)
        return response.json()

    def _configure(
        self, base_url: str, headers: dict, auth: AuthBase, errors: Set[Error]
    ):
        self.base_url = base_url
        self.headers = headers
        if self.auth is None:
            self.auth = auth
        self.errors = errors

    def __handle_error(self, response: Response):
        for error in self.errors:
            if error._is_error(response.status_code, response.json()):
                # this line raises an exception
                Request.__build_exception(error)

        # no defined error, use default one
        if response.status_code == 404:  # specific default error
            e = Error(
                404,
                f"Not Found. This is a default error thrown by sd_utils. The http url requested does not exist.",
            )
            e._set_api_name("not_found")
        else:
            e = Error(
                400,
                f"Bad Request. This is a default error thrown by sd_utils. This means that the error response was not defined or the request sent was invalid. Error code: {response.status_code}",
            )
            e._set_api_name("bad_request")
        Request.__build_exception(e)

    @staticmethod
    def __build_exception(error: Error):
        def constructor(self):
            super(Exception, self).__init__(f"[{error.code}] {error.message}")

        raise type(
            f"{error._api_name.replace('_', ' ').title().replace(' ', '')}",
            (Exception,),
            {"__init__": constructor},
        )


class GET(Request):
    def _make_request(
        self, query: str = "", body: dict = {}, headers: dict = {}
    ) -> Any:
        return super()._make_request("GET", query, body, headers)


class POST(Request):
    def _make_request(
        self, query: str = "", body: dict = {}, headers: dict = {}
    ) -> Any:
        return super()._make_request("POST", query, body, headers)


class PUT(Request):
    def _make_request(
        self, query: str = "", body: dict = {}, headers: dict = {}
    ) -> Any:
        return super()._make_request("PUT", query, body, headers)


class DELETE(Request):
    def _make_request(
        self, query: str = "", body: dict = {}, headers: dict = {}
    ) -> Any:
        return super()._make_request("DELETE", query, body, headers)
