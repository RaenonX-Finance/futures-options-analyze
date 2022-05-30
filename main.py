import glob
import re

import matplotlib.pyplot as plt
import pandas as pd

DATA_PATHS = glob.glob("data/*.csv")

MARGIN_X = 0.05
MARGIN_Y = 0.1

PLOT_WIDTH = 10
PLOT_HEIGHT = {
    "NQM22": 8,
    "ESM22": 5,
}

BAR_HEIGHT = {
    "NQM22": 50,
    "ESM22": 25,
}

SPACE = 0.17

FONT_SIZE_MAIN_TITLE = 16
FONT_SIZE_TITLE = 14
FONT_SIZE_LABEL = 13

PT_INTERVAL = {
    "NQM22": 100,
    "ESM22": 50,
}

STRIKE_LOW = {
    "NQM22": 11000,
    "ESM22": 3500,
}
STRIKE_HIGH = {
    "NQM22": 14000,
    "ESM22": 4500,
}

# ------------------


def get_file_props(data_path):
    _, path = data_path.split("\\")

    regex = r"(?P<Symbol>\w+)-.+-exp-(?P<Expiry>[\d_]+)-.+-(?P<DateM>\d{2})-(?P<DateD>\d{2})-(?P<DateY>\d{4})\.csv"

    props = list(re.finditer(regex, path))[0].groupdict()
    props = {
        "Symbol": props["Symbol"].upper(),
        "Expiry": props["Expiry"].replace("_", "/"),
        "Date": f"{props['DateM']}-{props['DateD']}-{props['DateY'][-2:]}"
    }

    return props


def get_plot_title(props):
    return f"{props['Symbol']} {props['Expiry']} (@{props['Date']})"


def get_config(props, config_body: float | int | dict[str, str | float]):
    if isinstance(config_body, (float, int)):
        return config_body

    if config := config_body.get(props["Symbol"]):
        return config

    return config_body["_"]


# ------------------


def get_data_def(data_path, props):
    df = pd.read_csv(data_path, thousands=",").iloc[:-1, :]
    df = df[df["Strike"] % get_config(props, PT_INTERVAL) == 0]
    df = df[
        (df["Strike"] >= get_config(props, STRIKE_LOW)) &
        (df["Strike"] <= get_config(props, STRIKE_HIGH))
    ]
    df.index = df["Strike"]
    df["Open Int - Call"] = df["Open Int"]
    df["Open Int - Put"] = df["Open Int.1"]

    return df


def main(data_path):
    props = get_file_props(data_path)
    df = get_data_def(data_path, props)

    font_color = "#525252"
    hfont = {"fontname": "Calibri"}
    face_color = "#eaeaf2"
    color_call = "#01b8aa"
    color_put = "#fd625e"
    index = df.index
    column_call = df["Open Int - Call"]
    column_put = df["Open Int - Put"]

    title_call = "Call OI"
    title_put = "Put OI"

    # noinspection PyTypeChecker
    fig, axes = plt.subplots(
        figsize=(get_config(props, PLOT_WIDTH), get_config(props, PLOT_HEIGHT)),
        facecolor=face_color, ncols=2, sharey=True
    )
    fig.tight_layout()

    axes[0].barh(
        index, column_call,
        align="center", color=color_call, height=get_config(props, BAR_HEIGHT)
    )
    axes[0].set_title(
        title_call, fontsize=get_config(props, FONT_SIZE_TITLE), color=color_call,
        **hfont
    )
    axes[1].barh(
        index, column_put,
        align="center", color=color_put, height=get_config(props, BAR_HEIGHT)
    )
    axes[1].set_title(
        title_put, fontsize=get_config(props, FONT_SIZE_TITLE), color=color_put,
        **hfont
    )

    # If you have positive numbers and want to invert the x-axis of the left plot
    axes[0].invert_xaxis()

    # To show data from highest to lowest
    plt.gca().invert_yaxis()

    axes[0].set(yticks=df.index, yticklabels=df.index)
    axes[0].yaxis.tick_right()
    axes[0].tick_params(axis="y", colors="white")  # tick color

    for label in (axes[0].get_xticklabels() + axes[0].get_yticklabels()):
        label.set(fontsize=get_config(props, FONT_SIZE_LABEL), color=font_color, **hfont)
    for label in (axes[1].get_xticklabels() + axes[1].get_yticklabels()):
        label.set(fontsize=get_config(props, FONT_SIZE_LABEL), color=font_color, **hfont)

    fig.suptitle(get_plot_title(props), fontsize=get_config(props, FONT_SIZE_MAIN_TITLE))
    plt.subplots_adjust(
        wspace=get_config(props, SPACE),
        top=1 - get_config(props, MARGIN_Y), bottom=get_config(props, MARGIN_Y),
        left=get_config(props, MARGIN_X), right=1 - get_config(props, MARGIN_X)
    )
    plt.show()


if __name__ == '__main__':
    for path in DATA_PATHS:
        main(path)
