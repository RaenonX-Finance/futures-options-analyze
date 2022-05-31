from dataclasses import dataclass
from typing import Literal


@dataclass
class FuturesOptionsProps:
    month_year: str
    product_id: int


FuturesOptionsPropNames = Literal[
    "NQM22 American",
    "ESM22 American",
]


FOP_PROPS: dict[FuturesOptionsPropNames, FuturesOptionsProps] = {
    "NQM22 American": FuturesOptionsProps(month_year="QZM22", product_id=148),
    "ESM22 American": FuturesOptionsProps(month_year="EZM22", product_id=138),
}
