import pandas as pd

from .const import PT_INTERVAL, STRIKE_HIGH, STRIKE_LOW
from .utils import get_config


def get_df(data_path, props):
    df = pd.read_csv(data_path, thousands=",").iloc[:-1, :]

    df = df[df["Strike"] % get_config(props, PT_INTERVAL) == 0]
    df = df[
        (df["Strike"] >= get_config(props, STRIKE_LOW)) &
        (df["Strike"] <= get_config(props, STRIKE_HIGH))
    ]
    df["OI Call"] = df["Open Int"]
    df["OI Put"] = df["Open Int.1"]

    df.index = df["Strike"]

    return df
