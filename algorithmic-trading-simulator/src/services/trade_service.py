# Executes buy and sell operations with transactional safeguards.

from decimal import Decimal, InvalidOperation
from fastapi import HTTPException, status


class TradeService:

    # Validate trade quantity
    @staticmethod
    def validate_quantity(quantity: Decimal) -> Decimal:

        try:
            quantity = Decimal(str(quantity))

        except (InvalidOperation, ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid quantity.",
            )

        if quantity <= Decimal("0"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero.",
            )

        return quantity

    # Validate price
    @staticmethod
    def validate_price(price: Decimal) -> Decimal:

        try:
            price = Decimal(str(price))

        except (InvalidOperation, ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid price.",
            )

        if price <= Decimal("0"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Price must be greater than zero.",
            )

        return price

    # Calculate total trade value
    @staticmethod
    def calculate_trade_value(
        quantity: Decimal,
        price: Decimal,
    ) -> Decimal:

        quantity = TradeService.validate_quantity(quantity)
        price = TradeService.validate_price(price)

        return quantity * price

    # Check if user can afford a buy order
    @staticmethod
    def validate_buy_balance(
        balance: Decimal,
        trade_value: Decimal,
    ) -> bool:

        if balance < trade_value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient wallet balance.",
            )

        return True

    # Check if user has enough assets to sell
    @staticmethod
    def validate_sell_quantity(
        available_quantity: Decimal,
        sell_quantity: Decimal,
    ):

        available_quantity = Decimal(str(available_quantity))
        sell_quantity = TradeService.validate_quantity(
            sell_quantity
        )

        if sell_quantity > available_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient asset quantity.",
            )

        return True
