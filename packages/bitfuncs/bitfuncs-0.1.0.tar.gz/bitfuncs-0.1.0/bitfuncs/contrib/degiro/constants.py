ALLOWED_DAY_RESOLUTIONS = ["P1D", "P7D", "P1M"]
ALLOWED_MIN_RESOLUTIONS = [f"PT{n}M" for n in (1, 2, 5, 15, 30, 60)]

ALLOWED_PERIODS = ["P1D", "P1W"]
ALLOWED_PERIODS += [f"P{n}M" for n in (1, 3, 6)]
ALLOWED_PERIODS += [f"P{n}Y" for n in (1, 3, 5, 50)]

DT_FMT_SEC = "%Y-%m-%dT%H:%M:%S"
