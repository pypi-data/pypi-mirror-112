import numpy as np
import pandas as pd
from backtesting import Strategy as _Strategy
from backtesting.lib import crossover
from talib import abstract as ta


def DERIV(values, fn=lambda x: x, index=None, **kw):
    res = fn(values, **kw)
    return pd.Series(res if index is None else res[index]).diff()


class Strategy(_Strategy):
    bbands_timeperiod = 5
    bbands_nbdevup = 2.0
    bbands_nbdevdn = 2.0
    bbands_matype = 0

    macd_fastperiod = 12
    macd_slowperiod = 26
    macd_signalperiod = 9

    rsi_timeperiod = 14
    sma_timeperiod = 20

    crossover_one = "rsi"
    crossover_two = 50

    def init(self):
        super().init()
        # upper, middle, lower = ta.BBANDS(...)
        # self.bbands = self.I(
        self.bbands_upper, self.bbands_middle, self.bbands_lower = self.I(
            ta.BBANDS,
            self.data.Close,
            timeperiod=int(self.bbands_timeperiod),
            nbdevup=self.bbands_nbdevup,
            nbdevdn=self.bbands_nbdevdn,
            matype=int(self.bbands_matype),
        )
        # macd, macdsignal, macdhist = talib.MACD(...)
        self.macd, self.macdsignal, self.macdhist = self.I(
            ta.MACD,
            self.data.Close,
            fastperiod=int(self.macd_fastperiod),
            slowperiod=int(self.macd_slowperiod),
            signalperiod=int(self.macd_signalperiod),
        )
        self.macd_hist_deriv = self.I(
            DERIV,
            self.data.Close,
            fn=ta.MACD,
            index=2,
            fastperiod=int(self.macd_fastperiod),
            slowperiod=int(self.macd_slowperiod),
            signalperiod=int(self.macd_signalperiod),
        )
        # rsi = talib.RSI(...)
        self.rsi = self.I(
            ta.RSI,
            self.data.Close,
            timeperiod=int(self.rsi_timeperiod),
        )
        # sma = talib.SMA(...)
        self.sma = self.I(
            ta.SMA,
            self.data.Close,
            timeperiod=int(self.sma_timeperiod),
        )

    def _getattr(self, attr_path):
        obj = self
        for attr in attr_path.split(":"):
            if isinstance(obj, dict):
                obj = obj[attr]
            else:
                obj = getattr(obj, attr)
        return obj

    def next(self):
        c_one = (
            int(self.crossover_one)
            if isinstance(self.crossover_one, (int, np.int64))
            else self._getattr(self.crossover_one)
        )

        c_two = (
            int(self.crossover_two)
            if isinstance(self.crossover_two, (int, np.int64))
            else self._getattr(self.crossover_two)
        )

        if crossover(c_one, c_two):
            self.buy()
        elif crossover(c_two, c_one):
            self.sell()
