import pandas as pd


def values_to_df(values):
    df = pd.DataFrame(reversed(values))
    df["time"] = pd.to_datetime(df["time"], format="%Y-%m-%dT%H:%M:%S")
    return df
