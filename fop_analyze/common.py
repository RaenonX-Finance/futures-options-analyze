import matplotlib.pyplot as plt

from .const import (
    FONT_SIZE_LABEL, FONT_SIZE_MAIN_TITLE, FONT_NAME_MAIN, FONT_COLOR,
    MARGIN_X, MARGIN_Y, SPACE
)
from .props import DataProperties
from .utils import get_config, get_plot_title


def format_plot(fig, axes, props: DataProperties, index):
    fig.tight_layout()

    # If you have positive numbers and want to invert the x-axis of the left plot
    axes[0].invert_xaxis()

    # To show data from highest to lowest
    plt.gca().invert_yaxis()

    x_ticks_left = axes[0].get_xticks()
    x_ticks_right = axes[1].get_xticks()

    x_max_left = x_ticks_left.max()
    x_max_right = x_ticks_right.max()

    if x_max_left > x_max_right:
        axes[0].set_xticks(x_ticks_left)
        axes[1].set_xticks(x_ticks_left)
    else:
        axes[0].set_xticks(x_ticks_right)
        axes[1].set_xticks(x_ticks_right)

    axes[0].set(yticks=index, yticklabels=index)
    axes[0].yaxis.tick_right()
    axes[0].tick_params(axis="y", colors="white")  # tick color

    for label in (axes[0].get_xticklabels() + axes[0].get_yticklabels()):
        label.set(
            fontsize=get_config(props, FONT_SIZE_LABEL), fontname=FONT_NAME_MAIN,
            color=FONT_COLOR,
        )
    for label in (axes[1].get_xticklabels() + axes[1].get_yticklabels()):
        label.set(
            fontsize=get_config(props, FONT_SIZE_LABEL), fontname=FONT_NAME_MAIN,
            color=FONT_COLOR,
        )

    fig.suptitle(
        get_plot_title(props),
        fontsize=get_config(props, FONT_SIZE_MAIN_TITLE)
    )

    plt.subplots_adjust(
        wspace=get_config(props, SPACE),
        top=1 - get_config(props, MARGIN_Y),
        bottom=get_config(props, MARGIN_Y),
        left=get_config(props, MARGIN_X),
        right=1 - get_config(props, MARGIN_X)
    )
    plt.tick_params(left=False)
    plt.show()
