from typing import Literal

from .props import FuturesOptionsProps


WEB_HEADERS = {
    "Accept-Language": "en",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/102.0.5005.62 Safari/537.36"
}

FuturesOptionsPropNames = Literal[
    "NQM22 American",
    "ESM22 American",
    "NQU22 American",
    "ESU22 American",
    "NQM22 Jun 22 W1",
    "ESM22 Jun 22 W1",
    "NQM22 Jun 22 W2",
    "ESM22 Jun 22 W2",
]

FOP_PROPS: dict[FuturesOptionsPropNames, FuturesOptionsProps] = {
    "NQM22 American": FuturesOptionsProps(month_year="QZM22", product_id=148),
    "ESM22 American": FuturesOptionsProps(month_year="EZM22", product_id=138),
    "NQU22 American": FuturesOptionsProps(month_year="QZU22", product_id=148),
    "ESU22 American": FuturesOptionsProps(month_year="EZU22", product_id=138),
    "NQM22 Jun 22 W1": FuturesOptionsProps(month_year="QN1M22", product_id=5395),
    "ESM22 Jun 22 W1": FuturesOptionsProps(month_year="EW1M22", product_id=2915),
    "NQM22 Jun 22 W2": FuturesOptionsProps(month_year="QN2M22", product_id=5396),
    "ESM22 Jun 22 W2": FuturesOptionsProps(month_year="EW2M22", product_id=2916),
}
