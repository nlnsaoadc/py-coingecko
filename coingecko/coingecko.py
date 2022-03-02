"""CoinGecko API wrapper.

Web: https://www.coingecko.com/en
Doc: https://www.coingecko.com/en/api/documentation
"""
import json
import logging
from typing import Any, Dict, List, Optional

import requests

from .utils import clean_params

logger = logging.getLogger(__name__)


class CoinGeckoAPIError(Exception):
    def __init__(self, response, message=""):
        super().__init__(message)
        self.response = response
        self.message = message

    def __str__(self):
        # try just in case there is no json available
        try:
            content = self.response.json()["error"]
        except json.JSONDecodeError:
            content = self.response.content.decode()
        return f"{self.response.status_code} {content}"


class CoinGecko:
    """CoinGecko API wrapper.

    Web: https://www.coingecko.com/en
    Doc: https://www.coingecko.com/en/api/documentation
    """

    BASE_URL = "https://api.coingecko.com/api/v3/"

    def __init__(
        self, key: Optional[str] = None, fail_silently: bool = False
    ) -> None:
        """Init the CoinGecko API.

        Args:
            key (:obj:`str`, optional): CoinGecko API key.
            fail_silently (:obj:`bool`, optional): If true an exception should
                be raise in case of wrong status code. Defaults to False.
        """
        self.key = key
        self.fail_silently = fail_silently

    def _get_headers(self) -> Dict[str, str]:
        return {"accept": "application/json"}

    def _get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Get requests to the specified path on CoinGecko API."""
        r = requests.get(
            url=self.BASE_URL + path,
            params=clean_params(params),
            headers=self._get_headers(),
        )

        if r.status_code == 200:
            return r.json()

        details = r.content.decode()
        try:
            details = r.json()
        except Exception:
            pass

        if not self.fail_silently:
            logger.warning(
                f"CoinGecko API error {r.status_code} on {path}: {details}"
            )
            self._fail(r)
        else:
            logger.info(
                f"CoinGecko API silent error {r.status_code} on {path}: "
                f"{details}"
            )
            return None

    def _fail(self, r):
        raise CoinGeckoAPIError(response=r)

    def ping(self):
        """Check API server status."""
        return self._get("ping")

    def get_simple_price(
        self,
        ids: List[str],
        vs_currencies: List[str],
        include_market_cap: Optional[bool] = None,
        include_24hr_vol: Optional[bool] = None,
        include_24hr_change: Optional[bool] = None,
        include_last_updated_at: Optional[bool] = None,
    ):
        """Get the current price of any crypto in any supported currencies."""
        return self._get(
            "simple/price",
            params={
                "ids": ids,
                "vs_currencies": vs_currencies,
                "include_market_cap": include_market_cap,
                "include_24hr_vol": include_24hr_vol,
                "include_24hr_change": include_24hr_change,
                "include_last_updated_at": include_last_updated_at,
            },
        )

    def get_simple_token_price(
        self,
        id: str,
        contract_addresses: List[str],
        vs_currencies: List[str],
        include_market_cap: Optional[bool] = None,
        include_24hr_vol: Optional[bool] = None,
        include_24hr_change: Optional[bool] = None,
        include_last_updated_at: Optional[bool] = None,
    ):
        """Get current price of tokens."""
        return self._get(
            "simple/token_price/{id}",
            params={
                "contract_addresses": contract_addresses,
                "vs_currencies": vs_currencies,
                "include_market_cap": include_market_cap,
                "include_24hr_vol": include_24hr_vol,
                "include_24hr_change": include_24hr_change,
                "include_last_updated_at": include_last_updated_at,
            },
        )

    def get_simple_supported_vs_currencies(self):
        """Get list of supported_vs_currencies."""
        return self._get("simple/supported_vs_currencies")

    def get_coins_list(self, include_platform: Optional[bool] = None):
        """Use this to obtain all the coins' id in order to make API calls."""
        return self._get(
            "coins/list",
            params={"include_platform": str(include_platform).lower()},
        )

    def get_coins_markets(
        self,
        vs_currency: str,
        ids: Optional[List[str]] = None,
        category: Optional[str] = None,
        order: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        sparkline: Optional[bool] = None,
        price_change_percentage: Optional[List[str]] = None,
    ):
        """Use this to obtain all the coins market data."""
        return self._get(
            "coins/markets",
            params={
                "vs_currency": vs_currency,
                "ids": ids,
                "category": category,
                "order": order,
                "per_page": per_page,
                "page": page,
                "sparkline": sparkline,
                "price_change_percentage": price_change_percentage,
            },
        )

    def get_coin_by_id(
        self,
        id: str,
        localization: Optional[bool] = False,
        tickers: Optional[bool] = False,
        market_data: Optional[bool] = None,
        community_data: Optional[bool] = None,
        developer_data: Optional[bool] = None,
        sparkline: Optional[bool] = None,
    ):
        """Get current data for a coin."""
        return self._get(
            f"coins/{id}",
            params={
                "localization": localization,
                "tickers": tickers,
                "market_data": market_data,
                "community_data": community_data,
                "developer_data": developer_data,
                "sparkline": sparkline,
            },
        )

    def get_coin_tickers(
        self,
        id: str,
        exchange_ids: Optional[str] = None,
        include_exchange_logo: Optional[str] = None,
        page: Optional[int] = None,
        order: Optional[str] = None,
        depth: Optional[str] = None,
    ):
        """Get coin tickers."""
        return self._get(
            f"coins/{id}/tickers",
            params={
                "exchange_ids": exchange_ids,
                "include_exchange_logo": include_exchange_logo,
                "page": page,
                "order": order,
                "depth": depth,
            },
        )

    def get_coin_history(
        self,
        id: str,
        date: str,
        localization: Optional[str] = None,
    ):
        """Get historical data."""
        return self._get(
            f"coins/{id}/history",
            params={
                "date": date,
                "localization": localization,
            },
        )

    def get_coin_market_chart(
        self,
        id: str,
        vs_currency: str,
        days: str,
        interval: Optional[str] = None,
    ):
        """Get historical market data."""
        return self._get(
            f"coins/{id}/market_chart",
            params={
                "vs_currency": vs_currency,
                "days": days,
                "interval": interval,
            },
        )

    def get_coin_market_chart_range(
        self,
        id: str,
        vs_currency: str,
        from_param: str,
        to: str,
    ):
        """Get historical market data."""
        return self._get(
            f"coins/{id}/market_chart/range",
            params={
                "vs_currency": vs_currency,
                "from": from_param,
                "to": to,
            },
        )

    def get_coin_status_updates(
        self,
        id: str,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        """Get status updates for a given coin."""
        return self._get(
            f"coins/{id}/market_chart/range",
            params={
                "per_page": per_page,
                "page": page,
            },
        )

    def get_coin_ohlc(
        self,
        id: str,
        vs_currency: str,
        days: str,
    ):
        """Get coin's OHLC."""
        return self._get(
            f"coins/{id}/ohlc",
            params={
                "vs_currency": vs_currency,
                "days": days,
            },
        )

    def get_coin_contract(self, id: str, contract_address: str):
        """Get coin info from contract address."""
        return self._get(f"coins/{id}/contract/{contract_address}")

    def get_coin_contract_market_chart(
        self,
        id: str,
        contract_address: str,
        vs_currency: str,
        days: str,
    ):
        """Get historical market data include."""
        return self._get(
            f"coins/{id}/contract/{contract_address}/market_chart/",
            params={
                "vs_currency": vs_currency,
                "days": days,
            },
        )

    def get_coin_contract_market_chart_range(
        self,
        id: str,
        contract_address: str,
        vs_currency: str,
        from_param: int,
        to: int,
    ):
        """Get historical market data include."""
        return self._get(
            f"coins/{id}/contract/{contract_address}/market_chart/",
            params={
                "vs_currency": vs_currency,
                "from": from_param,
                "to": to,
            },
        )

    def get_asset_platforms(self):
        """List all asset platforms."""
        return self._get("asset_platforms")

    def get_coin_categories_list(self):
        """List all categories."""
        return self._get("coins/categories/list")

    def get_coin_categories(self):
        """List all categories with market data."""
        return self._get("coins/categories")

    def get_exchanges(self):
        """List all exchanges."""
        return self._get("exchanges")

    def get_exchanges_list(self):
        """List all supported markets id and name."""
        return self._get("exchanges/list")

    def get_exchange(self, id: str):
        """Get exchange volume in BTC and tickers."""
        return self._get("exchanges/{id}")

    def get_exchange_tickets(
        self,
        id: str,
        coin_ids: Optional[List[str]] = None,
        include_exchange_logo: Optional[str] = None,
        page: Optional[int] = None,
        depth: Optional[str] = None,
        order: Optional[str] = None,
    ):
        """Get exchange tickers (paginated)."""
        return self._get(
            "exchanges/{id}/tickers",
            params={
                "coin_ids": coin_ids,
                "include_exchange_logo": include_exchange_logo,
                "page": page,
                "depth": depth,
                "order": order,
            },
        )

    def get_exchange_status_updates(
        self,
        id: str,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        """Get status updates for a given exchange."""
        return self._get(
            "exchanges/{id}/status_updates",
            params={
                "per_page": per_page,
                "page": page,
            },
        )

    def get_exchange_volume_chart(
        self,
        id: str,
        days: int,
    ):
        """Get volume_chart data for a given exchange."""
        return self._get(
            "exchanges/{id}/volume_chart",
            params={"days": days},
        )

    def get_finance_platforms(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        """List all finance platforms."""
        return self._get(
            "finance_platforms",
            params={"per_page": per_page, "page": page},
        )

    def get_finance_products(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        start_at: Optional[str] = None,
        end_at: Optional[str] = None,
    ):
        """List all finance platforms."""
        return self._get(
            "finance_platforms",
            params={
                "per_page": per_page,
                "page": page,
                "start_at": start_at,
                "end_at": end_at,
            },
        )

    def get_indexes(self):
        """List all market indexes."""
        return self._get("indexes")

    def get_indexes_by_market_id(self, market_id: str, id: str):
        """Get market index by market id and index id."""
        return self._get("indexes/{market_id}/{id}")

    def get_indexes_list(self):
        """List market indexes id and name."""
        return self._get("indexes/list")

    def get_derivatives(self):
        """List all derivative tickers."""
        return self._get("derivatives")

    def get_derivatives_exchanges(self):
        """List all derivative exchanges."""
        return self._get("derivatives/exchanges")

    def get_derivatives_exchange(
        self,
        id: str,
        include_tickers: Optional[str] = None,
    ):
        """Show derivative exchange data."""
        return self._get(
            "derivatives/exchanges/{id}",
            params={"include_tickers": include_tickers},
        )

    def get_derivatives_exchanges_list(self):
        """List all derivative exchanges name and identifier."""
        return self._get("derivatives/exchanges/list")

    def get_status_updates(
        self,
        category: Optional[str] = None,
        project_type: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ):
        """List all status_updates with data."""
        return self._get(
            "status_updates",
            params={
                "category": category,
                "project_type": project_type,
                "per_page": per_page,
                "page": page,
            },
        )

    def get_events(
        self,
        country_code: Optional[str] = None,
        event_type: Optional[str] = None,
        page: Optional[int] = None,
        upcoming_events_only: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ):
        """Get events, paginated by 100."""
        return self._get(
            "events",
            params={
                "country_code": country_code,
                "type": event_type,
                "page": page,
                "upcoming_events_only": upcoming_events_only,
                "from_date": from_date,
                "to_date": to_date,
            },
        )

    def get_events_countries(self):
        """Get list of event countries."""
        return self._get("events/countries")

    def get_events_types(self):
        """Get list of event types."""
        return self._get("events/types")

    def get_events_exchange_rates(self):
        """Get BTC-to-Currency exchange rates."""
        return self._get("exchange_rates")

    def get_search_trending(self):
        """Top-7 trending coins on CoinGecko as searched by users last 24h."""
        return self._get("search/trending")

    def get_global(self):
        """Get cryptocurrency global data."""
        return self._get("global")

    def get_global_decentralized_finance_defi(self):
        """Get Top 100 Cryptocurrency Global Decentralized Finance data."""
        return self._get("global/decentralized_finance_defi")

    def get_companies(self, coin_id: str):
        """Get public companies bitcoin or ethereum holdings."""
        return self._get("companies/public_treasury/{coin_id}")
