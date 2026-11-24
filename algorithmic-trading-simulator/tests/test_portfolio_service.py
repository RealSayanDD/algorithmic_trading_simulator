from decimal import Decimal
from types import SimpleNamespace

from src.models.transaction import TransactionSide
from src.services.portfolio_service import PortfolioService


def _make_tx(symbol: str, side: TransactionSide, quantity: str) -> SimpleNamespace:
    return SimpleNamespace(
        asset=SimpleNamespace(symbol=symbol),
        side=side,
        quantity=Decimal(quantity),
    )


def test_calculate_holdings_aggregates_buys_and_sells() -> None:
    transactions = [
        _make_tx("AAPL", TransactionSide.BUY, "10"),
        _make_tx("AAPL", TransactionSide.SELL, "4"),
        _make_tx("TSLA", TransactionSide.BUY, "2.5"),
        _make_tx("MSFT", TransactionSide.BUY, "5"),
        _make_tx("MSFT", TransactionSide.SELL, "5"),  # Should be removed (zero balance)
    ]

    holdings = PortfolioService.calculate_holdings(transactions)

    assert holdings == {
        "AAPL": Decimal("6"),
        "TSLA": Decimal("2.5"),
    }
    assert "MSFT" not in holdings


def test_calculate_holdings_empty() -> None:
    assert PortfolioService.calculate_holdings([]) == {}


def test_calculate_portfolio_value_and_missing_prices() -> None:
    holdings = {
        "AAPL": Decimal("2"),
        "TSLA": Decimal("1.5"),
        "UNKNOWN": Decimal("10"),
    }
    current_prices = {
        "AAPL": Decimal("150.25"),
        "TSLA": 200.50,
        # UNKNOWN intentionally omitted
    }

    value = PortfolioService.calculate_portfolio_value(holdings, current_prices)

    # (2 * 150.25) + (1.5 * 200.50) = 300.50 + 300.75 = 601.25
    assert value == Decimal("601.25")


def test_calculate_total_balance() -> None:
    total = PortfolioService.calculate_total_balance(
        wallet_balance=Decimal("1000.50"),
        portfolio_value=Decimal("601.25"),
    )
    assert total == Decimal("1601.75")