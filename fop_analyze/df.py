import pandas as pd
import requests

from .const import PT_INTERVAL, STRIKE_HIGH, STRIKE_LOW, TITLE_CALL, TITLE_PUT
from .props import DataProperties
from .utils import get_config
from .web import FuturesOptionsPropNames, WEB_HEADERS, make_url


def _filter_strike(df: pd.DataFrame, strike_col_name: str, props: DataProperties):
    df = df[df[strike_col_name] % get_config(props, PT_INTERVAL) == 0]
    df = df[
        (df[strike_col_name] >= get_config(props, STRIKE_LOW)) &
        (df[strike_col_name] <= get_config(props, STRIKE_HIGH))
    ]

    return df


def get_df_from_data(data_path: str, props: DataProperties):
    df = pd.read_csv(data_path, thousands=",").iloc[:-1, :]

    df = _filter_strike(df, "Strike", props)
    df["OI Call"] = df["Open Int"]
    df["OI Put"] = df["Open Int.1"]

    df.index = df["Strike"]

    return df


def get_df_from_web(prop_name: FuturesOptionsPropNames, trade_date: str, props: DataProperties):
    url = make_url(prop_name, trade_date)

    response = requests.get(url, headers=WEB_HEADERS)
    response.raise_for_status()

    response_content = response.json()

    data = response_content["settlements"]

    df = pd.DataFrame(data).iloc[:-1, :]
    df["openInterest"] = df["openInterest"].str.replace(",", "").astype(int)
    df["strike"] = df["strike"].astype(float)

    df = _filter_strike(df, "strike", props)

    df_call = df[df["type"] == "Call"].set_index("strike")
    df_put = df[df["type"] == "Put"].set_index("strike")

    df_merge = df_call.merge(df_put, suffixes=("", ".1"), left_index=True, right_index=True)
    df_merge[TITLE_CALL] = df_merge["openInterest"]
    df_merge[TITLE_PUT] = df_merge["openInterest.1"]

    return df_merge


def get_df_diff(df_main: pd.DataFrame, df_sub: pd.DataFrame):
    df_ret = df_main.merge(df_sub, suffixes=(" Main", " Sub"), left_index=True, right_index=True)
    df_ret["OI Call B"] = df_ret[["OI Call Main", "OI Call Sub"]].min(axis=1)
    df_ret["OI Call +"] = (df_ret["OI Call Main"] - df_ret["OI Call Sub"]).clip(lower=0)
    df_ret["OI Call -"] = (df_ret["OI Call Sub"] - df_ret["OI Call Main"]).clip(lower=0)
    df_ret["OI Put B"] = df_ret[["OI Put Main", "OI Put Sub"]].min(axis=1)
    df_ret["OI Put +"] = (df_ret["OI Put Main"] - df_ret["OI Put Sub"]).clip(lower=0)
    df_ret["OI Put -"] = (df_ret["OI Put Sub"] - df_ret["OI Put Main"]).clip(lower=0)

    return df_ret
