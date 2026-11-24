from decimal import Decimal

import pytest
from fastapi import HTTPException

from src.services.trade_service import TradeService


def test_validate_quantity_valid_and_invalid() -> None:
    assert TradeService.validate_quantity(Decimal("2.5")) == Decimal("2.5")

    with pytest.raises(HTTPException) as exc:
        TradeService.validate_quantity(Decimal("0"))
    assert exc.value.status_code == 400
    assert exc.value.detail == "Quantity must be greater than zero."

    with pytest.raises(HTTPException) as exc:
        TradeService.validate_quantity(Decimal("-3"))
    assert exc.value.status_code == 400

    with pytest.raises(HTTPException) as exc:
        TradeService.validate_quantity("abc")  # type: ignore[arg-type]
    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid quantity."


def test_validate_price_valid_and_invalid() -> None:
    assert TradeService.validate_price(Decimal("150.75")) == Decimal("150.75")

    with pytest.raises(HTTPException) as exc:
        TradeService.validate_price(Decimal("0"))
    assert exc.value.status_code == 400
    assert exc.value.detail == "Price must be greater than zero."

    with pytest.raises(HTTPException) as exc:
        TradeService.validate_price("not-a-price")  # type: ignore[arg-type]
    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid price."


def test_calculate_trade_value_decimal_precision() -> None:
    # Verifies exact Decimal arithmetic (no float rounding drift)
    value = TradeService.calculate_trade_value(Decimal("0.1"), Decimal("0.2"))
    assert value == Decimal("0.02")

    total = TradeService.calculate_trade_value(Decimal("3.25"), Decimal("100.40"))
    assert total == Decimal("326.3000")


def test_validate_buy_balance() -> None:
    assert TradeService.validate_buy_balance(Decimal("500.00"), Decimal("500.00")) is True
    assert TradeService.validate_buy_balance(Decimal("1000.00"), Decimal("250.50")) is True

    with pytest.raises(HTTPException) as exc:
        TradeService.validate_buy_balance(Decimal("100.00"), Decimal("100.01"))
    assert exc.value.status_code == 400
    assert exc.value.detail == "Insufficient wallet balance."


def test_validate_sell_quantity() -> None:
    assert TradeService.validate_sell_quantity(Decimal("10"), Decimal("10")) is True
    assert TradeService.validate_sell_quantity(Decimal("10"), Decimal("4.5")) is True

    with pytest.raises(HTTPException) as exc:
        TradeService.validate_sell_quantity(Decimal("5"), Decimal("5.01"))
    assert exc.value.status_code == 400
    assert exc.value.detail == "Insufficient asset quantity."