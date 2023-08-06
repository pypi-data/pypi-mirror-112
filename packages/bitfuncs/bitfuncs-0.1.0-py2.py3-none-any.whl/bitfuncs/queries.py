from asyncsql.queries import Queries

from .models import (
    StockIndicatorBBANDS,
    StockIndicatorMACD,
    StockIndicatorRSI,
    StockValue,
)

stock_indicators_bbands_queries = Queries(
    "stock_indicators_bbands",
    direction="desc",
    model_cls=StockIndicatorBBANDS,
    order_fields=("time",),
    returning_fields=("id",),
)

stock_indicators_macd_queries = Queries(
    "stock_indicators_macd",
    direction="desc",
    model_cls=StockIndicatorMACD,
    order_fields=("time",),
    returning_fields=("id",),
)

stock_indicators_rsi_queries = Queries(
    "stock_indicators_rsi",
    direction="desc",
    model_cls=StockIndicatorRSI,
    order_fields=("time",),
    returning_fields=("id",),
)

stock_values_queries = Queries(
    "stock_values",
    direction="desc",
    model_cls=StockValue,
    order_fields=("time",),
    returning_fields=("id",),
)

queries_registry = {
    "stock_indicators_bbands": stock_indicators_bbands_queries,
    "stock_indicators_macd": stock_indicators_macd_queries,
    "stock_indicators_rsi": stock_indicators_rsi_queries,
    "stock_values": stock_values_queries,
}
