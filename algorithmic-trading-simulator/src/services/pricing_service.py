
import os
import re
import httpx
from typing import Optional


class PricingService:
    """
    Service responsible for communicating with market data providers.
    """

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

        self.client = httpx.AsyncClient(
            timeout=10.0
        )

    def validate_symbol(self, symbol: str) -> bool:
        """
        Validate the format of an asset symbol.
        """
        if not symbol:
            return False

        symbol = symbol.strip().upper()

        # Allow letters, numbers, dots and hyphens.
        return bool(re.fullmatch(r"[A-Z0-9.-]{1,15}", symbol))

    def prepare_request_params(self, symbol: str) -> dict:
        """
        Prepare query parameters for the market data API.
        """
        return {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol.upper(),
            "apikey": self.api_key
        }

    async def make_request(self, params: dict) -> Optional[dict]:
        """
        Make an asynchronous HTTP request to the market data provider.
        """
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

    async def close(self):
        """
        Close the asynchronous HTTP client.
        """
        await self.client.aclose()
