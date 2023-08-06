from sd_utils.func import create_function
from flask.json import jsonify
from sd_utils.api.endpoint import Endpoint
from typing import Tuple
from sd_utils.api.provider import HttpProvider
from flask import Flask, request
from inspect import signature


ROUTE_NO = 0


class FlaskProvider(HttpProvider):
    def __init__(self, app: Flask):
        self.app = app

    def add_endpoint(self, url: str, method: str, endpoint: Endpoint):
        global ROUTE_NO

        def execute():
            return self.format_response(
                self._internal_handle(endpoint, request)
            )

        cloned = create_function(
            f"execute_{ROUTE_NO}", signature(execute), execute
        )
        ROUTE_NO += 1

        self.app.route(url, methods=[method])(cloned)

    def format_response(self, response: Tuple[int, dict]):
        return jsonify({"status_code": response[0], "data": response[1]})
