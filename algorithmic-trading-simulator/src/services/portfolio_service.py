
from decimal import Decimal
from collections import defaultdict

from src.models.transaction import TransactionSide


class PortfolioService:

    # Calculate current holdings from transaction history
    @staticmethod
    def calculate_holdings(transactions):

        holdings = defaultdict(Decimal)

        for transaction in transactions:

            symbol = transaction.asset.symbol

            if transaction.side == TransactionSide.BUY:
                holdings[symbol] += transaction.quantity

            elif transaction.side == TransactionSide.SELL:
                holdings[symbol] -= transaction.quantity

        # Remove assets with zero holdings
        holdings = {
            symbol: quantity
            for symbol, quantity in holdings.items()
            if quantity > Decimal("0")
        }

        return holdings

    # Calculate total value of holdings
    @staticmethod
    def calculate_portfolio_value(
        holdings,
        current_prices,
    ):

        total_value = Decimal("0")

        for symbol, quantity in holdings.items():

            price = current_prices.get(symbol)

            if price is None:
                continue

            price = Decimal(str(price))

            total_value += quantity * price

        return total_value

    # Calculate total portfolio balance
    @staticmethod
    def calculate_total_balance(
        wallet_balance,
        portfolio_value,
    ):

        wallet_balance = Decimal(str(wallet_balance))
        portfolio_value = Decimal(str(portfolio_value))

        return wallet_balance + portfolio_value
