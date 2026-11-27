from decimal import Decimal

import httpx
import pytest

from src.main import app
from src.services.pricing_service import PricingService


@pytest.mark.asyncio
async def test_get_asset_price_success_and_closes_client(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    close_called = False

    async def fake_get_stock_price(self: PricingService, symbol: str) -> float:
        assert symbol == "  aapl  "
        return 189.45

    async def fake_close(self: PricingService) -> None:
        nonlocal close_called
        close_called = True

    monkeypatch.setattr(PricingService, "get_stock_price", fake_get_stock_price)
    monkeypatch.setattr(PricingService, "close", fake_close)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/assets/%20%20aapl%20%20/price")

    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "AAPL"
    assert Decimal(str(payload["price"])) == Decimal("189.45")
    assert payload["currency"] == "USD"
    assert payload["source"] == "Alpha Vantage"
    assert close_called is True


@pytest.mark.asyncio
async def test_get_asset_price_returns_502_when_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    close_called = False

    async def fake_get_stock_price(self: PricingService, symbol: str) -> None:
        return None

    async def fake_close(self: PricingService) -> None:
        nonlocal close_called
        close_called = True

    monkeypatch.setattr(PricingService, "get_stock_price", fake_get_stock_price)
    monkeypatch.setattr(PricingService, "close", fake_close)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/assets/INVALID!/price")

    assert response.status_code == 502
    assert response.json()["detail"] == "Unable to retrieve market price."
    assert close_called is True


@pytest.mark.asyncio
async def test_get_asset_price_end_to_end_with_mocked_upstream(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test-key")

    def mock_alpha_vantage(request: httpx.Request) -> httpx.Response:
        assert request.url.params["symbol"] == "MSFT"
        return httpx.Response(
            200,
            json={"Global Quote": {"01. symbol": "MSFT", "05. price": "425.80"}},
        )

    original_init = PricingService.__init__

    def patched_init(self: PricingService) -> None:
        original_init(self)
        self.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_alpha_vantage))

    monkeypatch.setattr(PricingService, "__init__", patched_init)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/assets/msft/price")

    assert response.status_code == 200
    payload = response.json()
    assert payload["symbol"] == "MSFT"
    assert Decimal(str(payload["price"])) == Decimal("425.80")