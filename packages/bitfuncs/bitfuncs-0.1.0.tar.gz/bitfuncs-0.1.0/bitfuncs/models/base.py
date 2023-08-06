from datetime import datetime
from enum import Enum

from asyncsql.models import Model
from pydantic import validator


class ResolutionEnum(str, Enum):
    P1D = "P1D"
    P7D = "P7D"
    PT1M = "PT1M"
    PT2M = "PT2M"
    PT5M = "PT5M"
    PT15M = "PT15M"
    PT30M = "PT30M"
    PT60M = "PT60M"


class StockModel(Model):
    id: int = None
    symbol: str
    time: datetime
    resolution: ResolutionEnum

    @validator("time", pre=True)
    def id_must_be_date(cls, v):
        if isinstance(v, datetime):
            return v
        else:
            return datetime.fromisoformat(v)
