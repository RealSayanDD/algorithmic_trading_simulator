# Defines WebSocket endpoints for streaming price updates.
import asyncio
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import random

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws", tags=["websocket"])

# Initial simulated base prices for stocks and crypto
BASE_PRICES: dict[str, Decimal] = {
    "AAPL": Decimal("185.50"),
    "TSLA": Decimal("240.00"),
    "GOOGL": Decimal("175.25"),
    "BTC": Decimal("65000.00"),
    "ETH": Decimal("3400.00"),
}


def simulate_next_price(current_price: Decimal) -> Decimal:
    """Simulate a small realistic price movement (-0.5% to +0.5%)."""
    change_percent = Decimal(str(random.uniform(-0.005, 0.005)))
    new_price = current_price * (Decimal("1") + change_percent)
    return new_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@router.websocket("/prices/{symbol}")
async def stream_asset_price(websocket: WebSocket, symbol: str) -> None:
    """Stream simulated live price updates for a specific stock/crypto symbol."""
    symbol = symbol.upper()
    if symbol not in BASE_PRICES:
        await websocket.close(code=1008, reason=f"Unsupported symbol: {symbol}")
        return

    await websocket.accept()
    current_price = BASE_PRICES[symbol]

    try:
        while True:
            current_price = simulate_next_price(current_price)
            await websocket.send_json(
                {
                    "symbol": symbol,
                    "price": str(current_price),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass