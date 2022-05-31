import re

from .props import DataProperties


def get_file_props(data_path: str) -> DataProperties:
    _, path = data_path.split("\\")

    regex = r"(?P<Symbol>\w+)-.+-exp-(?P<Expiry>[\d_]+)-.+-(?P<DateM>\d{2})-(?P<DateD>\d{2})-(?P<DateY>\d{4})\.csv"

    props = list(re.finditer(regex, path))[0].groupdict()

    return DataProperties(
        symbol=props["Symbol"].upper(),
        expiry=props["Expiry"].replace("_", "/"),
        date=f"{props['DateM']}-{props['DateD']}-{props['DateY'][-2:]}",
    )


def get_plot_title(props: DataProperties):
    return f"{props.symbol} {props.expiry} (@{props.date})"


def get_config(props: DataProperties, config_body: float | int | dict[str, str | float]):
    if isinstance(config_body, (float, int)):
        return config_body

    if config := config_body.get(props.symbol):
        return config

    return config_body["_"]
