import logging
import os
from functools import partial, wraps

from backtesting import Backtest
from chamallow.decorators import flow

from ..contrib.backtesting.strategies import Strategy
from ..helpers import values_to_df

logger = logging.getLogger(__name__)


def with_bt():
    def with_df_decorator(func):
        @wraps(func)
        def func_wrapper(
            values,
            *a,
            cash=100000.0,
            commission=0.0025,
            exclusive_orders=True,
            trade_on_close=True,
            **kw,
        ):
            df = values_to_df(values)
            df.drop(["id", "symbol", "resolution"], axis=1, inplace=True)
            df.columns = ["time", "Open", "High", "Low", "Close", "Volume"]
            df.set_index("time", inplace=True)
            # --
            bt = Backtest(
                df,
                Strategy,
                cash=cash,
                commission=commission,
                exclusive_orders=exclusive_orders,
                trade_on_close=trade_on_close,
            )
            return func(bt, *a, **kw)

        return func_wrapper

    return with_df_decorator


@flow()
@with_bt()
def position(bt, params=None):
    params = params or {}
    params.pop("position", None)

    stats = bt.run(**params)
    size = stats._trades.iloc[-1]["Size"]

    if size:
        return "long"
    else:
        return "short"


@flow()
@with_bt()
def optimize(bt, crossover_args=()):
    optimize_func = bt.optimize

    if any(str(c).startswith("bbands_middle") for c in crossover_args):
        optimize_func = partial(
            optimize_func,
            bbands_timeperiod=range(3, 10, 2),
        )

    if any(str(c).startswith("macd") for c in crossover_args):
        optimize_func = partial(
            optimize_func,
            macd_fastperiod=range(4, 24, 4),
            macd_slowperiod=range(18, 38, 4),
            macd_signalperiod=range(1, 21, 4),
        )

    if any(str(c).startswith("rsi") for c in crossover_args):
        optimize_func = partial(
            optimize_func,
            rsi_timeperiod=range(6, 26, 4),
        )

    if any(str(c).startswith("sma") for c in crossover_args):
        optimize_func = partial(
            optimize_func,
            sma_timeperiod=range(12, 32, 4),
        )

    if crossover_args:
        crossover_one, crossover_two = crossover_args

        def _split(co):
            return [int(c) if c.isdigit() else c for c in str(co).split(",")]

        optimize_func = partial(
            optimize_func,
            crossover_one=_split(crossover_one),
            crossover_two=_split(crossover_two),
        )

    stats, heatmap = optimize_func(
        maximize="Equity Final [$]",
        return_heatmap=True,
    )

    best = heatmap.reset_index(name="equity").sort_values("equity").iloc[-1]
    best_dict = best.to_dict()
    best_dict.pop("equity")

    size = stats._trades.iloc[-1]["Size"]

    if size > 0:
        best_dict["position"] = "long"
    else:
        best_dict["position"] = "short"

    return best_dict


@flow()
@with_bt()
def plot(bt, name="out", outdir="./var", params=None):
    params = params or {}
    params.pop("position", None)

    bt.run(**params)

    path = os.path.join(outdir, f"{name}.html")
    bt.plot(filename=path, open_browser=False, plot_volume=False)

    return "done"
