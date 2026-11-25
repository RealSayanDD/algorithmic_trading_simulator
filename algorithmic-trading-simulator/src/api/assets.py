# Defines endpoints for listing assets and retrieving prices.

from decimal import Decimal

from fastapi import APIRouter, HTTPException, status

from src.schemas.asset import AssetPriceResponse
from src.services.pricing_service import PricingService


router = APIRouter(prefix="/api/assets", tags=["assets"])


@router.get("/{symbol}/price", response_model=AssetPriceResponse)
async def get_asset_price(symbol: str):

    pricing_service = PricingService()

    try:
        price = await pricing_service.get_stock_price(symbol)

        if price is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unable to retrieve market price."
            )

        return AssetPriceResponse(
            symbol=symbol.strip().upper(),
            price=Decimal(str(price))
        )

    finally:
        await pricing_service.close()
