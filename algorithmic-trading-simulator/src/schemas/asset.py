# Validates asset details and market price data.

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class AssetPriceResponse(BaseModel):
    symbol: str
    price: Decimal
    currency: str = "USD"
    source: str = "Alpha Vantage"

    model_config = ConfigDict(from_attributes=True)
