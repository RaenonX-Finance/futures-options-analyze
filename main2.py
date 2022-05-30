import matplotlib.pyplot as plt

from fop_analyze.common import format_plot
from fop_analyze.const import (
    BAR_HEIGHT, COLOR_CALL, COLOR_PUT, COLOR_INCREASE, COLOR_DECREASE,
    FACE_COLOR, FONT_NAME_MAIN, FONT_SIZE_TITLE,
    PLOT_HEIGHT, PLOT_WIDTH, TITLE_CALL, TITLE_PUT,
)
from fop_analyze.df import get_df
from fop_analyze.utils import get_config, get_file_props

# Main should be the latest data

DATA_PATH_MAIN = "data\\nqm22-options-eom-options-exp-05_31_22-show-all-side-by-side-intraday-05-29-2022.csv"
DATA_PATH_SUB = "data\\nqm22-options-american-options-exp-06_17_22-show-all-side-by-side-intraday-05-29-2022.csv"


def get_data_df(data_path_main, data_path_sub, props):
    df_main = get_df(data_path_main, props)
    df_sub = get_df(data_path_sub, props)

    df_ret = df_main.merge(df_sub, suffixes=(" Main", " Sub"), left_index=True, right_index=True)
    df_ret["OI Call B"] = df_ret[["OI Call Main", "OI Call Sub"]].min(axis=1)
    df_ret["OI Call +"] = (df_ret["OI Call Main"] - df_ret["OI Call Sub"]).clip(lower=0)
    df_ret["OI Call -"] = (df_ret["OI Call Sub"] - df_ret["OI Call Main"]).clip(lower=0)
    df_ret["OI Put B"] = df_ret[["OI Put Main", "OI Put Sub"]].min(axis=1)
    df_ret["OI Put +"] = (df_ret["OI Put Main"] - df_ret["OI Put Sub"]).clip(lower=0)
    df_ret["OI Put -"] = (df_ret["OI Put Sub"] - df_ret["OI Put Main"]).clip(lower=0)

    return df_ret


def main(data_path_main, data_path_sub):
    props = get_file_props(data_path_main)
    df = get_data_df(data_path_main, data_path_sub, props)

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
    main(DATA_PATH_MAIN, DATA_PATH_SUB)
