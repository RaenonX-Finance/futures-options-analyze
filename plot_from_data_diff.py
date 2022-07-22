import matplotlib.pyplot as plt

from fop_analyze.common import format_plot
from fop_analyze.const import (
    BAR_HEIGHT, COLOR_CALL, COLOR_PUT, COLOR_INCREASE, COLOR_DECREASE,
    FACE_COLOR, FONT_NAME_MAIN, FONT_SIZE_TITLE,
    PLOT_HEIGHT, PLOT_WIDTH, TITLE_CALL, TITLE_PUT,
)
from fop_analyze.df import get_df_from_data, get_df_diff
from fop_analyze.props import DataProperties
from fop_analyze.utils import get_config, get_file_props

# Main should be the latest data

# NQU22 Aug W1 22
# > https://www.barchart.com/futures/quotes/NQU22/options/MW1Q22?moneyness=allRows&futuresOptionsView=split
# NQU22 Jul EOM 22
# > https://www.barchart.com/futures/quotes/NQU22/options/MQ6N22?moneyness=allRows&futuresOptionsView=split
# NQU22 American
# > https://www.barchart.com/futures/quotes/NQU22/options?futuresOptionsView=split&moneyness=allRows
# ESU22 Aug W1 22
# > https://www.barchart.com/futures/quotes/ESU22/options/MW1Q22?moneyness=allRows&futuresOptionsView=split
# ESU22 Jul EOM 22
# > https://www.barchart.com/futures/quotes/ESU22/options/T8N22?moneyness=allRows&futuresOptionsView=split
# ESU22 American
# > https://www.barchart.com/futures/quotes/ESU22/options?futuresOptionsView=split&moneyness=allRows

MAIN_DATE: str = "07-22-2022"
SUB_DATE: str = "07-21-2022"

DATA_PATHS: list[(str, str)] = [
    (
        f"data\\esu22-options-eom-options-exp-07_29_22-show-all-side-by-side-intraday-{MAIN_DATE}.csv",
        f"data\\esu22-options-eom-options-exp-07_29_22-show-all-side-by-side-intraday-{SUB_DATE}.csv"
    ),
    (
        f"data\\nqu22-options-eom-options-exp-07_29_22-show-all-side-by-side-intraday-{MAIN_DATE}.csv",
        f"data\\nqu22-options-eom-options-exp-07_29_22-show-all-side-by-side-intraday-{SUB_DATE}.csv"
    ),
    (
        f"data\\esu22-options-friday-weekly-options-exp-07_22_22-show-all-side-by-side-intraday-{MAIN_DATE}.csv",
        f"data\\esu22-options-friday-weekly-options-exp-07_22_22-show-all-side-by-side-intraday-{SUB_DATE}.csv"
    ),
    (
        f"data\\nqu22-options-friday-weekly-options-exp-07_22_22-show-all-side-by-side-intraday-{MAIN_DATE}.csv",
        f"data\\nqu22-options-friday-weekly-options-exp-07_22_22-show-all-side-by-side-intraday-{SUB_DATE}.csv"
    ),
    (
        f"data\\esu22-options-american-options-exp-09_16_22-show-all-side-by-side-intraday-{MAIN_DATE}.csv",
        f"data\\esu22-options-american-options-exp-09_16_22-show-all-side-by-side-intraday-{SUB_DATE}.csv"
    ),
    (
        f"data\\nqu22-options-american-options-exp-09_16_22-show-all-side-by-side-intraday-{MAIN_DATE}.csv",
        f"data\\nqu22-options-american-options-exp-09_16_22-show-all-side-by-side-intraday-{SUB_DATE}.csv"
    ),
]

SAVE_DIR: str = r"D:\UserData\Downloads"


def get_data_df(data_path_main: str, data_path_sub: str, props: DataProperties):
    df_main = get_df_from_data(data_path_main, props)
    df_sub = get_df_from_data(data_path_sub, props)

    return get_df_diff(df_main, df_sub)


def main(data_path_main: str, data_path_sub: str):
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

    format_plot(fig, axes, props, index, save_file_path=rf"{SAVE_DIR}\{props.save_file_name}.png")


if __name__ == '__main__':
    for path_main, path_sub in DATA_PATHS:
        main(path_main, path_sub)
