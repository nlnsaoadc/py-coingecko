import json
from unittest import TestCase, mock

from coingecko.coingecko import CoinGecko


class CoinGeckoTestCase(TestCase):
    def setUp(self):
        self.api = CoinGecko()

    def test_get_headers(self):
        headers = self.api._get_headers()
        self.assertIsNotNone(headers["accept"])

    @mock.patch(
        "requests.get", return_value=mock.Mock(status_code=200, json=lambda: {})
    )
    def test_get(self, mock_get):
        self.api._get("test")
        mock_get.assert_called_once_with(
            url="https://api.coingecko.com/api/v3/test",
            params=None,
            headers={"accept": "application/json"},
        )

    @mock.patch("coingecko.coingecko.logger.warning")
    @mock.patch(
        "requests.get",
        return_value=mock.Mock(
            status_code=404,
            json=lambda: {"error": "Not Found"},
            content=b"404 Not Found Message",
        ),
    )
    def test_get_404_status(self, mock_get, mock_log):
        with self.assertRaises(Exception) as context:
            self.api._get("test")
        self.assertEqual(
            "404 Not Found",
            str(context.exception),
        )
        mock_log.assert_called_once()

    @mock.patch("coingecko.coingecko.logger.info")
    @mock.patch(
        "requests.get",
        return_value=mock.Mock(
            status_code=404,
            json=mock.Mock(side_effect=Exception("")),
            content=b"404 Not Found Message",
        ),
    )
    def test_get_404_status_fail_silently(self, mock_get, mock_log):
        self.api.fail_silently = True
        self.assertEqual(self.api._get("test"), None)
        mock_log.assert_called_once()

    def test_fail_with_no_json(self):
        response = mock.Mock(
            status_code=404,
            content=b"Not Found Message Content",
        )
        response.json.side_effect = mock.Mock(
            side_effect=json.JSONDecodeError("msg", "doc", 0)
        )
        with self.assertRaises(Exception) as context:
            self.api._fail(response)
        self.assertEqual(
            "404 Not Found Message Content",
            str(context.exception),
        )

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_ping(self, mock_get):
        self.api.ping()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_simple_price(self, mock_get):
        self.api.get_simple_price(
            ids=["bitcoin", "ethereum"], vs_currencies=["usd"]
        )
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_simple_token_price(self, mock_get):
        self.api.get_simple_token_price(
            id="bitcoin", contract_addresses=[""], vs_currencies=[""]
        )
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_simple_supported_vs_currencies(self, mock_get):
        self.api.get_simple_supported_vs_currencies()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coins_list(self, mock_get):
        self.api.get_coins_list(include_platform=None)
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coins_markets(self, mock_get):
        self.api.get_coins_markets(vs_currency="eur")
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coin_by_id(self, mock_get):
        self.api.get_coin_by_id(id="bitcoin", localization=False, tickers=False)
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coin_tickers(self, mock_get):
        self.api.get_coin_tickers(
            id="bitcoin",
        )
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coin_history(self, mock_get):
        self.api.get_coin_history(id="bitcoin", date="")
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coin_market_chart(self, mock_get):
        self.api.get_coin_market_chart(id="bitcoin", vs_currency="", days="")
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coin_market_chart_range(self, mock_get):
        self.api.get_coin_market_chart_range(
            id="bitcoin", vs_currency="", from_param="", to=""
        )
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coin_status_updates(self, mock_get):
        self.api.get_coin_status_updates(id="bitcoin")
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coin_ohlc(self, mock_get):
        self.api.get_coin_ohlc(id="bitcoin", vs_currency="", days="")
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coin_contract(self, mock_get):
        self.api.get_coin_contract(id="bitcoin", contract_address="")
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coin_contract_market_chart(self, mock_get):
        self.api.get_coin_contract_market_chart(
            id="bitcoin", contract_address="", vs_currency="eur", days=""
        )
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coin_contract_market_chart_range(self, mock_get):
        self.api.get_coin_contract_market_chart_range(
            id="bitcoin",
            contract_address="",
            vs_currency="",
            from_param=1,
            to=1,
        )
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_asset_platforms(self, mock_get):
        self.api.get_asset_platforms()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coin_categories_list(self, mock_get):
        self.api.get_coin_categories_list()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_coin_categories(self, mock_get):
        self.api.get_coin_categories()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_exchanges(self, mock_get):
        self.api.get_exchanges()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_exchanges_list(self, mock_get):
        self.api.get_exchanges_list()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_exchange(self, mock_get):
        self.api.get_exchange(id="bitcoin")
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_exchange_tickets(self, mock_get):
        self.api.get_exchange_tickets(
            id="bitcoin",
        )
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_exchange_status_updates(self, mock_get):
        self.api.get_exchange_status_updates(id="bitcoin")
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_exchange_volume_chart(self, mock_get):
        self.api.get_exchange_volume_chart(id="bitcoin", days=1)
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_finance_platforms(self, mock_get):
        self.api.get_finance_platforms()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_finance_products(self, mock_get):
        self.api.get_finance_products()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_indexes(self, mock_get):
        self.api.get_indexes()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_indexes_by_market_id(self, mock_get):
        self.api.get_indexes_by_market_id(market_id="bitcoin", id="bitcoin")
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_indexes_list(self, mock_get):
        self.api.get_indexes_list()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_derivatives(self, mock_get):
        self.api.get_derivatives()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_derivatives_exchanges(self, mock_get):
        self.api.get_derivatives_exchanges()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_derivatives_exchange(self, mock_get):
        self.api.get_derivatives_exchange(id="bitcoin")
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_derivatives_exchanges_list(self, mock_get):
        self.api.get_derivatives_exchanges_list()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_status_updates(self, mock_get):
        self.api.get_status_updates()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_events(self, mock_get):
        self.api.get_events()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_events_countries(self, mock_get):
        self.api.get_events_countries()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_events_types(self, mock_get):
        self.api.get_events_types()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_events_exchange_rates(self, mock_get):
        self.api.get_events_exchange_rates()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_search_trending(self, mock_get):
        self.api.get_search_trending()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_global(self, mock_get):
        self.api.get_global()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_global_decentralized_finance_defi(self, mock_get):
        self.api.get_global_decentralized_finance_defi()
        mock_get.assert_called_once()

    @mock.patch("coingecko.coingecko.CoinGecko._get")
    def test_get_companies(self, mock_get):
        self.api.get_companies(coin_id="bitcoin")
        mock_get.assert_called_once()
