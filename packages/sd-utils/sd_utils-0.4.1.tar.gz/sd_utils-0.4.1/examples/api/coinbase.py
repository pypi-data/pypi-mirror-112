from sd_utils.api.error import Error
import time
import hmac
import hashlib
from requests.auth import AuthBase
from sd_utils.api.client import client_api
from sd_utils.api.request import GET


class CoinbaseAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = (
            timestamp
            + request.method
            + request.path_url
            + (request.body or "")
        )
        signature = hmac.new(
            bytes(self.secret_key, "latin-1"),
            bytes(message, "latin-1"),
            hashlib.sha256,
        ).hexdigest()

        request.headers.update(
            {
                "CB-ACCESS-SIGN": signature,
                "CB-ACCESS-TIMESTAMP": timestamp,
                "CB-ACCESS-KEY": self.api_key,
            }
        )
        return request


@client_api("https://api.coinbase.com/v2")
class Coinbase:
    # endpoints
    spot_price = GET("prices")
    time = GET("time")

    # this specific request fails, to demonstrate
    # error handling in the test suite
    # this is also one way you might provide
    # authentication to an endpoint
    user = GET(
        "user", auth=CoinbaseAuth('a "valid" api key', 'a "valid" api secret')
    )

    # errors
    invalid_token = Error(
        401,
        "Invalid Oauth token",
        lambda status_code, content: content["errors"][0]["id"]
        == "invalid_token",
    )
    authentication_error = Error(
        401,
        "Authentication Error",
        lambda status_code, content: content["errors"][0]["id"]
        == "authentication_error",
    )
