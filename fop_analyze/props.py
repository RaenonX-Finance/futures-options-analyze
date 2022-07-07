from dataclasses import dataclass


@dataclass
class DataProperties:
    symbol: str
    expiry: str
    date: str

    @property
    def save_file_name(self) -> str:
        return f"{self.symbol}-{self.expiry}@{self.date}".replace("\\", "").replace("/", "")
