# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pricehist', 'pricehist.outputs', 'pricehist.resources', 'pricehist.sources']

package_data = \
{'': ['*']}

install_requires = \
['cssselect>=1.1.0,<2.0.0',
 'curlify>=2.2.1,<3.0.0',
 'lxml>=4.6.2,<5.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['pricehist = pricehist.cli:cli']}

setup_kwargs = {
    'name': 'pricehist',
    'version': '0.1.4',
    'description': 'Fetch and format historical price data',
    'long_description': "# pricehist\n\nA command-line tool for fetching and formatting historical price data, with\nsupport for multiple data sources and output formats.\n\n## Installation\n\nInstall via [pip](https://pip.pypa.io/en/stable/) or\n[pipx](https://pypa.github.io/pipx/):\n\n```bash\npipx install pricehist\n```\n\n## Sources\n\n- **`alphavantage`**: [Alpha Vantage](https://www.alphavantage.co/)\n- **`coindesk`**: [CoinDesk Bitcoin Price Index](https://www.coindesk.com/coindesk-api)\n- **`coinmarketcap`**: [CoinMarketCap](https://coinmarketcap.com/)\n- **`ecb`**: [European Central Bank Euro foreign exchange reference rates](https://www.ecb.europa.eu/stats/exchange/eurofxref/html/index.en.html)\n- **`yahoo`**: [Yahoo! Finance](https://finance.yahoo.com/)\n\n## Output formats\n\n- **`beancount`**: [Beancount](http://furius.ca/beancount/)\n- **`csv`**: [Comma-separated values](https://en.wikipedia.org/wiki/Comma-separated_values)\n- **`gnucash-sql`**: [GnuCash](https://www.gnucash.org/) SQL\n- **`ledger`**: [Ledger](https://www.ledger-cli.org/) and [hledger](https://hledger.org/)\n\n## Examples\n\nShow usage information:\n\n```bash\npricehist -h\n```\n```\nusage: pricehist [-h] [--version] [--verbose] {sources,source,fetch} ...\n\nFetch historical price data\n\noptional arguments:\n  -h, --help              show this help message and exit\n  --version               show version information\n  --verbose               show all log messages\n\ncommands:\n  {sources,source,fetch}\n    sources               list sources\n    source                show source details\n    fetch                 fetch prices\n```\n\nShow usage information for the `fetch` command:\n\n```\npricehist fetch -h\n```\n```\nusage: pricehist fetch SOURCE PAIR [-h] [-t TYPE] [-s DATE | -sx DATE] [-e DATE | -ex DATE]\n[-o beancount|csv|gnucash-sql|ledger] [--invert] [--quantize INT]\n[--fmt-base SYM] [--fmt-quote SYM] [--fmt-time TIME] [--fmt-decimal CHAR] [--fmt-thousands CHAR]\n[--fmt-symbol rightspace|right|leftspace|left] [--fmt-datesep CHAR] [--fmt-csvdelim CHAR]\n\npositional arguments:\n  SOURCE                   the source identifier\n  PAIR                     pair, usually BASE/QUOTE, e.g. BTC/USD\n\noptional arguments:\n  -h, --help               show this help message and exit\n  -t TYPE, --type TYPE     price type, e.g. close\n  -s DATE, --start DATE    start date, inclusive (default: source start)\n  -sx DATE, --startx DATE  start date, exclusive\n  -e DATE, --end DATE      end date, inclusive (default: today)\n  -ex DATE, --endx DATE    end date, exclusive\n  -o FMT, --output FMT     output format (default: csv)\n  --invert                 invert the price, swapping base and quote\n  --quantize INT           round to the given number of decimal places\n  --fmt-base SYM           rename the base symbol in output\n  --fmt-quote SYM          rename the quote symbol in output\n  --fmt-time TIME          set a particular time of day in output (default: 00:00:00)\n  --fmt-decimal CHAR       decimal point in output (default: '.')\n  --fmt-thousands CHAR     thousands separator in output (default: '')\n  --fmt-symbol LOCATION    commodity symbol placement in output (default: rightspace)\n  --fmt-datesep CHAR       date separator in output (default: '-')\n  --fmt-csvdelim CHAR      field delimiter for CSV output (default: ',')\n```\n\nFetch prices after 2021-01-04, ending 2021-01-15, as CSV:\n\n```bash\npricehist fetch ecb EUR/AUD -sx 2021-01-04 -e 2021-01-15 -o csv\n```\n```\ndate,base,quote,amount,source,type\n2021-01-05,EUR,AUD,1.5927,ecb,reference\n2021-01-06,EUR,AUD,1.5824,ecb,reference\n2021-01-07,EUR,AUD,1.5836,ecb,reference\n2021-01-08,EUR,AUD,1.5758,ecb,reference\n2021-01-11,EUR,AUD,1.5783,ecb,reference\n2021-01-12,EUR,AUD,1.5742,ecb,reference\n2021-01-13,EUR,AUD,1.5734,ecb,reference\n2021-01-14,EUR,AUD,1.5642,ecb,reference\n2021-01-15,EUR,AUD,1.568,ecb,reference\n```\n\nIn Ledger format:\n\n```bash\npricehist fetch ecb EUR/AUD -s 2021-01-01 -o ledger | head\n```\n```\nP 2021-01-04 00:00:00 EUR 1.5928 AUD\nP 2021-01-05 00:00:00 EUR 1.5927 AUD\nP 2021-01-06 00:00:00 EUR 1.5824 AUD\nP 2021-01-07 00:00:00 EUR 1.5836 AUD\nP 2021-01-08 00:00:00 EUR 1.5758 AUD\nP 2021-01-11 00:00:00 EUR 1.5783 AUD\nP 2021-01-12 00:00:00 EUR 1.5742 AUD\nP 2021-01-13 00:00:00 EUR 1.5734 AUD\nP 2021-01-14 00:00:00 EUR 1.5642 AUD\nP 2021-01-15 00:00:00 EUR 1.568 AUD\n```\n\nGenerate SQL for a GnuCash database and apply it immediately:\n\n```bash\npricehist fetch ecb EUR/AUD -s 2021-01-01 -o gnucash-sql | sqlite3 Accounts.gnucash\npricehist fetch ecb EUR/AUD -s 2021-01-01 -o gnucash-sql | mysql -u username -p -D databasename\npricehist fetch ecb EUR/AUD -s 2021-01-01 -o gnucash-sql | psql -U username -d databasename -v ON_ERROR_STOP=1\n```\n\n## Design choices\n\nTo keep things simple, at least for now, `pricehist` provides only univariate\ntime series of daily historical prices. It doesn't provide other types of\nmarket, financial or economic data, real-time prices, or other temporal\nresolutions. Multiple or multivariate series require multiple invocations.\n\n## Alternatives\n\nBeancount's [`bean-price`](https://github.com/beancount/beanprice) tool fetches\nprices and addresses other workflow concerns in a Beancount-specific manner,\ngenerally requiring a Beancount file as input.\n\nThe [Piecash](https://piecash.readthedocs.io/) library is a pythonic interface\nto GnuCash files stored in SQL which has a\n[`Commodity.update_prices`](https://piecash.readthedocs.io/en/master/api/piecash.core.commodity.html?highlight=update_prices#piecash.core.commodity.Commodity.update_prices)\nmethod for fetching historical prices.\nThe GnuCash wiki documents [wrapper scripts](https://wiki.gnucash.org/wiki/Stocks/get_prices)\nfor the [Finance::QuoteHist](https://metacpan.org/pod/Finance::QuoteHist) Perl\nmodule.\n\nOther projects with related goals include:\n\n* [`hledger-stockquotes`](https://github.com/prikhi/hledger-stockquotes):\n  A CLI addon for hledger that reads a journal file and pulls the historical prices for commodities.\n* [`ledger_get_prices`](https://github.com/nathankot/ledger-get-prices):\n  Uses Yahoo Finance to generate a price database based on your current Ledger commodities and time period.\n* [LedgerStockUpdate](https://github.com/adchari/LedgerStockUpdate):\n  Locates any stocks you have in your ledger-cli file, then generates a price database of those stocks.\n* [`market-prices`](https://github.com/barrucadu/hledger-scripts#market-prices):\n  Downloads market values of commodities from a few different sources.\n",
    'author': 'Chris Berkhout',
    'author_email': 'chris@chrisberkhout.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/chrisberkhout/pricehist',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
