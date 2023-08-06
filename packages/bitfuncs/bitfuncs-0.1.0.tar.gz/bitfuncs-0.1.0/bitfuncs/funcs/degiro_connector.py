import logging
from datetime import datetime
from functools import partial

from chamallow import flow
from degiro_connector.quotecast.api import API as QuotecastAPI
from degiro_connector.quotecast.pb.quotecast_pb2 import Chart, Quotecast
from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.helpers import payload_handler
from degiro_connector.trading.pb.trading_pb2 import Credentials, ProductSearch

from ..contrib.degiro.chart_parser import chart_to_values
from ..decorators import json_cached
from ..settings import settings

logger = logging.getLogger(__name__)


class Backend:
    _config = None
    _quotecast_api = None
    _trading_api = None

    @json_cached(key="degiro-connector-config", ttl=30 * 60)
    async def _get_config(self):
        logger.info("get config for: %s", settings.degiro_username)
        return self.trading_api.get_config()

    @json_cached(key="degiro-connector-client-details", ttl=30 * 60)
    async def _client_details(self):
        logger.info("get client_details for: %s", settings.degiro_username)
        return self.trading_api.get_client_details()

    @property
    async def client_details(self):
        return await self._client_details()

    @property
    async def config(self):
        return await self._get_config()

    @property
    async def quotecast_api(self):
        if not self._quotecast_api:
            config = await self.config
            user_token = config["clientId"]
            self._quotecast_api = QuotecastAPI(user_token=user_token)
        return self._quotecast_api

    @property
    def trading_api(self):
        if not self._trading_api:
            credentials = Credentials(
                int_account=settings.degiro_int_account,
                username=settings.degiro_username,
                password=settings.degiro_password,
            )
            self._trading_api = TradingAPI(credentials=credentials)
            self._trading_api.connect()
        return self._trading_api


backend = Backend()


def key_builder(kind, f, key, *a, **kw):
    # can be stock info dict
    if isinstance(key, dict):
        key = key["symbol"].lower()
    return f"degiro-connector-{kind}-{key}"


@flow()
@json_cached(key_builder=partial(key_builder, "stock-info"))
async def get_stock_info(symbol):
    logger.info("get stock info for: %s", symbol)

    request_lookup = ProductSearch.RequestStocks(
        stock_country_id=886,
        offset=0,
        limit=1,
        search_text=symbol,
        require_total=True,
    )

    products_lookup = backend.trading_api.product_search(
        request=request_lookup, raw=False
    )
    products_lookup_dict = payload_handler.message_to_dict(message=products_lookup)

    if not products_lookup_dict["total"]:
        logger.warning("No stock info for: %s", symbol)

    return products_lookup_dict["products"][0]


def get_ticker_date(ticker):
    return (
        datetime.fromtimestamp(ticker["LastDate"] + ticker["LastTime"]).isoformat()[:10]
        + "T00:00:00"
    )


@flow()
async def get_ticker(stock_info):
    request = Quotecast.Request()
    request.subscriptions[stock_info["vwdId"]].extend(
        [
            "LastDate",
            "LastTime",
            "LastPrice",
            "LastVolume",
            "LastPrice",
            "AskPrice",
            "BidPrice",
        ]
    )
    quotecast_api = await backend.quotecast_api
    return quotecast_api.fetch_metrics(
        request=request,
    )[stock_info["vwdId"]]


@flow()
async def get_values(stock_info, last_date=None, resolution="P1D"):
    issueid = stock_info["vwdId"]

    request = Chart.Request()
    request.culture = "fr-FR"
    request.requestid = "1"
    request.series.append(f"issueid:{issueid}")
    request.series.append(f"ohlc:issueid:{issueid}")
    request.series.append(f"volume:issueid:{issueid}")
    request.tz = "Europe/Paris"

    if resolution == "P1D":
        period = "P6M"
    elif resolution.startswith("PT"):
        period = "P1W"
    else:
        raise RuntimeError(f"Unsupported resolution: {resolution}")

    quotecast_api = await backend.quotecast_api

    chart = quotecast_api.get_chart(
        request=request,
        override={
            "period": period,
            "resolution": resolution,
        },
        raw=True,
    )

    if isinstance(last_date, datetime):
        last_date = last_date.isoformat()

    if isinstance(last_date, str):
        last_date = last_date[:19]

    return [
        v
        for v in chart_to_values(chart, resolution=resolution)
        if not last_date or v["time"] > last_date
    ]
