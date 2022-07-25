import glob

import matplotlib.pyplot as plt

from fop_analyze.const import (
    PLOT_HEIGHT, PLOT_WIDTH, BAR_HEIGHT, FONT_SIZE_TITLE,
    FACE_COLOR, COLOR_CALL, COLOR_PUT, TITLE_CALL, TITLE_PUT, FONT_NAME_MAIN,
)
from fop_analyze.common import format_plot
from fop_analyze.df import get_df_from_data
from fop_analyze.utils import get_config, get_file_props

DATA_PATHS = glob.glob("data/nqu22-*-07-25-2022.csv")


def main(data_path: str):
    props = get_file_props(data_path)
    df = get_df_from_data(data_path, props)

    index = df.index
    column_call = df[TITLE_CALL]
    column_put = df[TITLE_PUT]

    # noinspection PyTypeChecker
    fig, axes = plt.subplots(
        figsize=(get_config(props, PLOT_WIDTH), get_config(props, PLOT_HEIGHT)),
        facecolor=FACE_COLOR, ncols=2, sharey=True
    )

    axes[0].barh(
        index, column_call,
        align="center", color=COLOR_CALL, height=get_config(props, BAR_HEIGHT)
    )
    axes[0].set_title(
        TITLE_CALL, fontsize=get_config(props, FONT_SIZE_TITLE), fontname=FONT_NAME_MAIN,
        color=COLOR_CALL,
    )
    axes[1].barh(
        index, column_put,
        align="center", color=COLOR_PUT, height=get_config(props, BAR_HEIGHT)
    )
    axes[1].set_title(
        TITLE_PUT, fontsize=get_config(props, FONT_SIZE_TITLE), fontname=FONT_NAME_MAIN,
        color=COLOR_PUT,
    )

    format_plot(fig, axes, props, index)


if __name__ == '__main__':
    for path in DATA_PATHS:
        main(path)
