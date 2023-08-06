from sd_utils.api.service import service
from sd_utils.api.impl.flask import FlaskProvider
from flask.app import Flask
from sd_utils.api.endpoint import Callback, Endpoint, QueryParam


class RsiEndpoint(Endpoint):
    crypto = QueryParam(str, True, "BTC")
    discord_hook = Callback("mydiscord-webhook", lambda x: None)


app = Flask(__name__)


@service(FlaskProvider(app))
class CryptoAnalysisService:
    rsi = RsiEndpoint()
    # note underscores will be converted to a /
    # that means this path is /rsi/past
    rsi_past = Endpoint(
        params={
            "crypto": QueryParam(str, False, "BTC"),
            "start_date": QueryParam(str, False, "01-03-2000"),
        },
        callbacks=[Callback("mydiscord-webhook", lambda u, x: None)],
        handle_fn=lambda x: (503, {"message": "different server error"}),
    )
