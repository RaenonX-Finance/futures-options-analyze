from datetime import datetime, time

import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = r"D:/UserData/Downloads/CME_MINI_MNQU2022, 15_fc041.csv"

df = pd.read_csv(DATA_PATH)
df["time"] = pd.to_datetime(df["time"]).dt.tz_localize(None)
df["date"] = df["time"].dt.date

df_dict = {date: df[:][df["date"] == date].copy() for date in df["date"].unique()}


def main():
    month = 6

    fig, ax = plt.subplots(6, 7, figsize=(21.14, 15))
    fig.patch.set_facecolor("#FEFEFE")

    for selected_date, date_df in df_dict.items():
        if selected_date.month != month:
            continue

        plot = df_dict[selected_date].plot.line(
            x="time",
            y="close",
            ax=ax[(selected_date.day - selected_date.weekday() + 7) // 7, selected_date.weekday()],
            legend=None,
            title=selected_date,
        )
        plot.axvspan(
            datetime.combine(selected_date, time(0, 0)),
            datetime.combine(selected_date, time(8, 30)),
            facecolor="#FF9800",
            alpha=0.25
        )
        plot.axvspan(
            datetime.combine(selected_date, time(15, 0)),
            datetime.combine(selected_date, time(23, 59, 59)),
            facecolor="#673AB7",
            alpha=0.25
        )

    for axe in ax.flat:
        axe.axes.xaxis.set_visible(False)
        axe.axes.yaxis.set_visible(False)


if __name__ == '__main__':
    main()
