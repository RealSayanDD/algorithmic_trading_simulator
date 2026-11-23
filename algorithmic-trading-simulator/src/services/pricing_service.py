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

        return bool(
            re.fullmatch(r"[A-Z0-9.-]{1,15}", symbol)
        )

    # Prepare API parameters
    def prepare_request_params(self, symbol: str) -> dict:

        return {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol.strip().upper(),
            "apikey": self.api_key,
        }

    # Perform async HTTP request
    async def make_request(
        self,
        params: dict,
    ) -> Optional[dict]:

        try:
            response = await self.client.get(
                self.BASE_URL,
                params=params,
            )

            response.raise_for_status()

            return response.json()

        except httpx.TimeoutException:
            print("Market API request timed out.")

        except httpx.HTTPStatusError as exc:
            print(
                f"HTTP error: {exc.response.status_code}"
            )

        except httpx.RequestError as exc:
            print(f"Network error: {exc}")

        except ValueError:
            print("Invalid JSON received.")

        return None

    # Detect API errors
    def check_api_error(
        self,
        data: dict,
    ) -> Optional[str]:

        if not data:
            return "Empty response received."

        if "Error Message" in data:
            return data["Error Message"]

        if "Note" in data:
            return "API rate limit exceeded."

        if "Information" in data:
            return data["Information"]

        return None

    # Retrieve stock price
    async def get_stock_price(
        self,
        symbol: str,
    ) -> Optional[float]:

        if not self.validate_symbol(symbol):
            print("Invalid stock symbol.")
            return None

        if not self.api_key:
            print("API key is missing.")
            return None

        params = self.prepare_request_params(symbol)

        data = await self.make_request(params)

        if not data:
            return None

        error = self.check_api_error(data)

        if error:
            print(f"Market API error: {error}")
            return None

        quote = data.get("Global Quote")

        if not quote:
            print("Quote data not found.")
            return None

        price = quote.get("05. price")

        if price is None:
            print("Price field is missing.")
            return None

        try:
            price = float(price)

            if price <= 0:
                return None

            return price

        except (ValueError, TypeError):
            print("Invalid price received.")
            return None

    # Close HTTP client
    async def close(self):
        await self.client.aclose()
