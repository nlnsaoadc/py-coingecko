# [CoinGecko API](https://www.coingecko.com/en) wrapper

[![py-coingecko-client-pypi](https://img.shields.io/pypi/v/py-coingecko-client.svg)](https://pypi.python.org/pypi/py-coingecko-client)

CoinGecko Doc: https://www.coingecko.com/en/api/documentation

## Install

```bash
pip install py-coingecko-client
```

## Usage

```python
from coingecko import CoinGecko

cg = CoinGecko()
cg.get_simple_price(ids=["bitcoin"], vs_currencies=["usd"])
```

## Testing

```bash
virtualenv venv
source ./venv/bin/activate
pip install -r dev_requirements.txt
deactivate
source ./venv/bin/activate
pytest
```
