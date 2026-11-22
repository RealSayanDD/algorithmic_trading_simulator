import httpx
import pytest

from src.services.pricing_service import PricingService


def test_validate_symbol() -> None:
    service = PricingService()
    assert service.validate_symbol("AAPL") is True
    assert service.validate_symbol("brk.b") is True
    assert service.validate_symbol("") is False
    assert service.validate_symbol("INVALID SYMBOL!") is False


def test_prepare_request_params_strips_whitespace(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test-key")
    service = PricingService()
    params = service.prepare_request_params("  aapl  ")
    assert params["symbol"] == "AAPL"
    assert params["function"] == "GLOBAL_QUOTE"
    assert params["apikey"] == "test-key"


def test_check_api_error_cases() -> None:
    service = PricingService()
    assert service.check_api_error({}) == "Empty response received."
    assert service.check_api_error({"Error Message": "Invalid API call."}) == "Invalid API call."
    assert service.check_api_error({"Note": "Limit reached"}) == "API rate limit exceeded. Please try again later."
    assert service.check_api_error({"Information": "Premium endpoint"}) == "Premium endpoint"
    assert service.check_api_error({"Global Quote": {"05. price": "150.00"}}) is None


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


@pytest.mark.asyncio
async def test_get_stock_price_handles_api_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test-key")

    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"Note": "API call frequency exceeded."})

    service = PricingService()
    service.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))

    price = await service.get_stock_price("AAPL")
    await service.close()

    assert price is None


@pytest.mark.asyncio
async def test_get_stock_price_rejects_zero_or_negative_price(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test-key")

    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"Global Quote": {"05. price": "-10.50"}})

    service = PricingService()
    service.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))

    price = await service.get_stock_price("AAPL")
    await service.close()

    assert price is None


@pytest.mark.asyncio
async def test_get_stock_price_rejects_non_numeric_price(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test-key")

    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"Global Quote": {"05. price": "N/A"}})

    service = PricingService()
    service.client = httpx.AsyncClient(transport=httpx.MockTransport(mock_handler))

    price = await service.get_stock_price("AAPL")
    await service.close()

    assert price is None