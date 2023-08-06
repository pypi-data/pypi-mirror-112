from .base import StockModel


class StockIndicatorBBANDS(StockModel):
    timeperiod: int
    nbdevup: int
    nbdevdn: int
    matype: int
    u: float
    m: float
    l: float


class StockIndicatorMACD(StockModel):
    fastperiod: int
    slowperiod: int
    signalperiod: int
    m: float
    ms: float
    mh: float


class StockIndicatorRSI(StockModel):
    timeperiod: int
    r: float
