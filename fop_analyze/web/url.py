from .props import FOP_PROPS, FuturesOptionsPropNames


def make_url(prop_name: FuturesOptionsPropNames, trade_date: str):
    """`trade_date` has to be in the format of MM/DD/YYYY."""
    prop = FOP_PROPS[prop_name]

    return f"https://www.cmegroup.com/CmeWS/mvc/Settlements/Options/Settlements/{prop.product_id}/OOF?" \
           f"optionProductId={prop.product_id}&monthYear={prop.month_year}&tradeDate={trade_date}"
