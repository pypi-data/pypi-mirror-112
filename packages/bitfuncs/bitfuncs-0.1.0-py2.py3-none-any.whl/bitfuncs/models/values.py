from .base import StockModel


class StockValue(StockModel):
    o: float = None
    h: float = None
    l: float = None
    c: float = None
    v: float = None
