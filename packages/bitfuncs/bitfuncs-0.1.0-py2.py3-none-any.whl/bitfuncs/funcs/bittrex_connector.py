import asyncio
import atexit
import logging
from datetime import datetime
from functools import partial

from aiobittrex import BittrexAPI
from chamallow import flow

from ..decorators import json_cached
from ..settings import settings

logger = logging.getLogger(__name__)


backend = BittrexAPI(
    api_key=settings.bittrex_api_key,
    api_secret=settings.bittrex_api_secret,
)


def key_builder(kind, f, key, *a, **kw):
    # can be crypto info dict
    if isinstance(key, dict):
        key = key["symbol"].lower()
    return f"bittrex-connector-{kind}-{key}"


@flow()
@json_cached(key_builder=partial(key_builder, "crypto-info"))
async def get_crypto_info(symbol):
    logger.info("get crypto info for: %s", symbol)
    return await backend.get_market_summary(f"USDT-{symbol}")


@flow()
async def get_ticker(symbol):
    ticker = await backend.get_ticker(f"USDT-{symbol}")
    return (ticker["Ask"] + ticker["Bid"]) / 2.0


def get_current_date(resolution):
    now = datetime.now()

    if resolution == "P1D":
        return (
            datetime(
                now.year,
                now.month,
                now.day,
            ).isoformat(),
            "day",
        )
    elif resolution == "PT60M":
        return (
            datetime(
                now.year,
                now.month,
                now.day,
                now.hour,
            ).isoformat(),
            "hour",
        )
    elif resolution == "PT1M":
        return (
            datetime(
                now.year,
                now.month,
                now.day,
                now.hour,
                now.minute,
            ).isoformat(),
            "oneMin",
        )
    else:
        raise RuntimeError("resolution not supported")


@flow()
async def get_values(symbol, last_date=None, resolution="P1D"):
    """
    resolution: oneMin(PT1M),fiveMin(no), hour(PT60M), day(P1D)
    """
    current_date, interval = get_current_date(resolution)
    values = await backend.get_candles(f"USDT-{symbol}", interval)
    return [
        {
            "o": v["O"],
            "h": v["H"],
            "l": v["L"],
            "c": v["C"],
            "v": v["V"],
            "time": v["T"],
        }
        for v in values
        if (not last_date or v["T"] > last_date) and v["T"] < current_date
    ]


atexit.register(partial(asyncio.run, backend.close()))
