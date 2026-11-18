import os
import httpx
from typing import Optional


class PricingService:
    """
    Handles communication with external market data providers.
    """

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        # Read the API key from environment variables.
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

        # Create an asynchronous HTTP client.
        self.client = httpx.AsyncClient(timeout=10.0)

    async def get_stock_price(self, symbol: str) -> Optional[float]:
        """
        Fetch the latest stock price for a given symbol.

        Actual API integration will be implemented in Week 2.
        """
        # TODO: Implement Alpha Vantage API request.

        return None

    async def close(self):
        """
        Close the HTTP client when it is no longer needed.
        """
        await self.client.aclose()
# Fetches and processes external market price data.
