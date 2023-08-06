# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coinmetrics']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.6.0,<4.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['poetry = poetry.console:run']}

setup_kwargs = {
    'name': 'coinmetrics-api-client',
    'version': '2021.7.8.14.9',
    'description': 'Python client for Coin Metrics API v4.',
    'long_description': '# Coin Metrics Python API v4 client library\n\nThis is an official Python API client for Coin Metrics API v4.\n\n## Installation\nTo install the client you can run the following command:\n```\npip install coinmetrics-api-client\n```\n\n\n## Introduction\nYou can use this client for querying all kinds of data with your API.\n\nTo initialize the client you should use your API key, and the CoinMetricsClient class like the following.\n```\nfrom coinmetrics.api_client import CoinMetricsClient\n\nclient = CoinMetricsClient(environ.get("CM_API_KEY"))\n\n# or to use community API:\nclient = CoinMetricsClient()\n```\n\nAfter that you can use the client object for getting stuff like available markets:\n```\nprint(client.catalog_markets())\n```\n\nor to query all available assets along with what is available for those assets, like metrics, markets:\n\n```\nprint(client.catalog_assets())\n```\n\n\nyou can also use filters for the catalog endpoints like this:\n\n```\nprint(client.catalog_assets(assets=[\'btc\']))\n```\nin this case you would get all the information for btc only\n\nYou can use this client to connect to our API v4 and get catalog or timeseries data from python environment. It natively supports paging over the data so you can use it to iterate over timeseries entries seamlessly.\n\nThe client can be used to query both pro and community data.\n\n## Getting timeseries data\n\nFor getting timeseries data you want to use methods of the client class that start with `get_`.\n\nFor example if you want to get a bunch of market data trades for coinbase btc-usd pair you can run something similar to the following:\n\n```\nfor trade in client.get_market_trades(markets=\'coinbase-btc-usd-spot\', \n                                      start_time=\'2020-01-01\', end_time=\'2020-01-03\'):\n    print(trade)\n```\n\nOr if you want to see daily btc asset metrics you can use something like this:\n\n```\nfor metric_data in client.get_asset_metrics(assets=\'btc\', \n                                            metrics=[\'ReferenceRateUSD\', \'BlkHgt\', \'AdrActCnt\',  \n                                                     \'AdrActRecCnt\', \'FlowOutBFXUSD\'], \n                                            frequency=\'1d\'):\n    print(metric_data)\n```\nThis will print you the requested metrics for all the days where we have any of the metrics present. \n\n### Paging\nYou can make the datapoints to iterate from start or from end (default).\n\nfor that you should use a paging_from argument like the following:\n```\nfrom coinmetrics.api_client import CoinMetricsClient\nfrom coinmetrics.constants import PagingFrom\n\nclient = CoinMetricsClient()\n\nfor metric_data in client.get_asset_metrics(assets=\'btc\', metrics=[\'ReferenceRateUSD\'],\n                                            paging_from=PagingFrom.START):\n    print(metric_data)\n```\n\nPagingFrom.END: is available but it is also a default value also, so you might not want to set it.\n\n## Extended documentation\nFor more information about the available methods in the client please reference [API Client Spec]([https://coinmetrics-io.github.io/api-client-python/site/api_client.html])\n',
    'author': 'Coin Metrics',
    'author_email': 'info@coinmetrics.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://coinmetrics-io.github.io/api-client-python/site/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
