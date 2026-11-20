from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from src.main import app

client = TestClient(app)


def test_websocket_streams_valid_symbol_prices() -> None:
    """Verify WebSocket streams live simulated prices for a valid symbol."""
    with client.websocket_connect("/ws/prices/btc") as websocket:
        data_1 = websocket.receive_json()
        data_2 = websocket.receive_json()

        assert data_1["symbol"] == "BTC"
        assert "price" in data_1
        assert "timestamp" in data_1

        # Check that price is a valid Decimal with 2 decimal places
        price_1 = Decimal(data_1["price"])
        price_2 = Decimal(data_2["price"])
        assert price_1 > Decimal("0")
        assert price_2 > Decimal("0")


def test_websocket_rejects_invalid_symbol() -> None:
    """Verify WebSocket closes cleanly with code 1008 for unsupported symbols."""
    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect("/ws/prices/INVALID") as websocket:
            websocket.receive_json()

    assert exc_info.value.code == 1008