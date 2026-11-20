
import os
import re
import httpx
from typing import Optional


class PricingService:

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.client = httpx.AsyncClient(timeout=10.0)

    # Validate stock symbol format
    def validate_symbol(self, symbol: str) -> bool:
        if not symbol:
            return False

        symbol = symbol.strip().upper()

        return bool(re.fullmatch(r"[A-Z0-9.-]{1,15}", symbol))

    # Prepare API request parameters
    def prepare_request_params(self, symbol: str) -> dict:
        return {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol.upper(),
            "apikey": self.api_key
        }

    # Make asynchronous API request
    async def make_request(self, params: dict) -> Optional[dict]:
        try:
            response = await self.client.get(
                self.BASE_URL,
                params=params
            )

            response.raise_for_status()

            return response.json()

        except httpx.TimeoutException:
            print("Market data API request timed out.")

        except httpx.HTTPStatusError as exc:
            print(f"HTTP error occurred: {exc.response.status_code}")

        except httpx.RequestError as exc:
            print(f"Request failed: {exc}")

        except ValueError:
            print("Invalid JSON response received.")

        return None

    # Retrieve the current stock price
    async def get_stock_price(self, symbol: str) -> Optional[float]:

        if not self.validate_symbol(symbol):
            print("Invalid stock symbol.")
            return None

        if not self.api_key:
            print("Alpha Vantage API key is missing.")
            return None

        params = self.prepare_request_params(symbol)

        data = await self.make_request(params)

        if not data:
            return None

        # Extract Global Quote information
        quote = data.get("Global Quote")

        if not quote:
            print("No stock price data found.")
            return None

        # Extract the price from the API response
        price = quote.get("05. price")

        if not price:
            print("Price information is missing.")
            return None

        try:
            return float(price)

        except (ValueError, TypeError):
            print("Invalid price received from API.")
            return None

    # Close the HTTP client
    async def close(self):
        await self.client.aclose()
