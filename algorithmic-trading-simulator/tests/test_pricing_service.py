import httpx
import pytest

from src.services.pricing_service import PricingService


def test_validate_symbol() -> None:
    service = PricingService()
    assert service.validate_symbol("AAPL") is True
    assert service.validate_symbol("brk.b") is True
    assert service.validate_symbol("") is False
    assert service.validate_symbol("INVALID SYMBOL!") is False


@pytest.mark.asyncio
async def test_get_stock_price_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test-key")

    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"Global Quote": {"01. symbol": "AAPL", "05. price": "189.45"}},
        )

    service = PricingService()
    service.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))

    price = await service.get_stock_price("aapl")
    await service.close()

    assert price == 189.45


@pytest.mark.asyncio
async def test_get_stock_price_missing_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ALPHA_VANTAGE_API_KEY", raising=False)
    service = PricingService()

    price = await service.get_stock_price("AAPL")
    await service.close()

    assert price is None


@pytest.mark.asyncio
async def test_get_stock_price_handles_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test-key")

    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "server error"})

    service = PricingService()
    service.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))

    price = await service.get_stock_price("AAPL")
    await service.close()

    assert price is None