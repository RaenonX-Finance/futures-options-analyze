import re


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
