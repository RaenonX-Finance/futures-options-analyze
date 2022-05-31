import matplotlib.pyplot as plt

from fop_analyze.common import format_plot
from fop_analyze.const import (
    BAR_HEIGHT, COLOR_CALL, COLOR_PUT, COLOR_INCREASE, COLOR_DECREASE,
    FACE_COLOR, FONT_NAME_MAIN, FONT_SIZE_TITLE,
    PLOT_HEIGHT, PLOT_WIDTH, TITLE_CALL, TITLE_PUT,
)
from fop_analyze.df import get_df_from_web, get_df_diff
from fop_analyze.props import DataProperties
from fop_analyze.utils import get_config
from fop_analyze.web import FuturesOptionsPropNames

# Main date should be the latest
# Note that OIs are prior day OIs, meaning that setting main date to 05/31 actually grabs the OI at 05/27.

FOP_NAME: FuturesOptionsPropNames = "ESM22 American"
FOP_EXPIRY: str = "06/17/22"

MAIN_DATE: str = "05/31/2022"
SUB_DATE: str = "05/27/2022"


def get_data_df(props: DataProperties):
    df_main = get_df_from_web(FOP_NAME, MAIN_DATE, props)
    df_sub = get_df_from_web(FOP_NAME, SUB_DATE, props)

    df_ret = df_main.merge(df_sub, suffixes=(" Main", " Sub"), left_index=True, right_index=True)
    df_ret["OI Call B"] = df_ret[["OI Call Main", "OI Call Sub"]].min(axis=1)
    df_ret["OI Call +"] = (df_ret["OI Call Main"] - df_ret["OI Call Sub"]).clip(lower=0)
    df_ret["OI Call -"] = (df_ret["OI Call Sub"] - df_ret["OI Call Main"]).clip(lower=0)
    df_ret["OI Put B"] = df_ret[["OI Put Main", "OI Put Sub"]].min(axis=1)
    df_ret["OI Put +"] = (df_ret["OI Put Main"] - df_ret["OI Put Sub"]).clip(lower=0)
    df_ret["OI Put -"] = (df_ret["OI Put Sub"] - df_ret["OI Put Main"]).clip(lower=0)

    return get_df_diff(df_main, df_sub)


def main():
    props = DataProperties(
        symbol=FOP_NAME.split(" ")[0],
        expiry=FOP_EXPIRY,
        date=MAIN_DATE,
    )
    df = get_data_df(props)

    index = df.index
    column_call_base = df["OI Call B"]
    column_call_inc = df["OI Call +"]
    column_call_dec = df["OI Call -"]
    column_put_base = df["OI Put B"]
    column_put_inc = df["OI Put +"]
    column_put_dec = df["OI Put -"]

    # noinspection PyTypeChecker
    fig, axes = plt.subplots(
        figsize=(get_config(props, PLOT_WIDTH), get_config(props, PLOT_HEIGHT)),
        facecolor=FACE_COLOR, ncols=2, sharey=True
    )

    bar_height = get_config(props, BAR_HEIGHT)

    axes[0].barh(
        index, column_call_base,
        align="center", color=COLOR_CALL, height=bar_height,
    )
    axes[0].barh(
        index, column_call_inc,
        left=column_call_base,
        align="center", color=COLOR_INCREASE, height=bar_height,
    )
    axes[0].barh(
        index, column_call_dec,
        left=column_call_base,
        align="center", color=COLOR_DECREASE, height=bar_height,
    )
    axes[0].set_title(
        TITLE_CALL, fontsize=get_config(props, FONT_SIZE_TITLE), color=COLOR_CALL,
        fontname=FONT_NAME_MAIN
    )

    axes[1].barh(
        index, column_put_base,
        align="center", color=COLOR_PUT, height=bar_height,
    )
    axes[1].barh(
        index, column_put_inc,
        left=column_put_base,
        align="center", color=COLOR_INCREASE, height=bar_height,
    )
    axes[1].barh(
        index, column_put_dec,
        left=column_put_base,
        align="center", color=COLOR_DECREASE, height=bar_height,
    )
    axes[1].set_title(
        TITLE_PUT,
        fontsize=get_config(props, FONT_SIZE_TITLE),
        color=COLOR_PUT,
    )

    format_plot(fig, axes, props, index)


if __name__ == '__main__':
    main()
