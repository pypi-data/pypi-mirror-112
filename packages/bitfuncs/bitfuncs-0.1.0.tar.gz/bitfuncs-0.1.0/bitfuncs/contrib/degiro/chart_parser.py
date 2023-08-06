import logging
from collections import defaultdict
from datetime import datetime, timedelta
from math import floor

from .constants import ALLOWED_DAY_RESOLUTIONS, ALLOWED_MIN_RESOLUTIONS, DT_FMT_SEC

logger = logging.getLogger(__name__)


def chart_to_values(chart, resolution="P1D"):
    if resolution == "P1M":
        raise RuntimeError("P1M resolution not supported yet")

    elif resolution in ALLOWED_DAY_RESOLUTIONS:
        delta_key = "days"
        delta_mul = int(resolution[1])

    elif resolution in ALLOWED_MIN_RESOLUTIONS:
        delta_key = "minutes"
        delta_mul = int(resolution[2:-1])

    def get_data(kind):
        for serie in chart["series"]:
            if serie["id"].startswith(kind):
                return serie["data"]

    start_date = datetime.strptime(chart["start"][:19], DT_FMT_SEC)
    values_dict = defaultdict(dict)

    for kind in ["volume", "ohlc"]:
        for delta, *values in get_data(kind):
            dt = start_date + timedelta(**{delta_key: floor(delta) * delta_mul})
            dt_str = dt.isoformat()

            first_key = kind[0]

            if first_key in values_dict.get(dt_str, {}):
                logger.info(
                    "skipped [%s] %s (already has %s)",
                    dt_str,
                    values,
                    values_dict[dt_str],
                )
                continue

            values_dict[dt_str]["time"] = dt_str

            if len(values) == 1:
                values_dict[dt_str][first_key] = values[0]
            else:
                values_dict[dt_str].update(dict(zip(kind, values)))

    return list(values_dict.values())
