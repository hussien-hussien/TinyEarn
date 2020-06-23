# TinyEarn - Webscraper for Zacks.com

TinyEarn is an simple selenium-based webscaper to pull earnings data from zacks.com. It navigates to 

Requirements:
* Python3
* Firefox Browser

## Usage
===========

There is one public function in the ``TinyEarn`` Class: ``get_earnings()``. It stores not private variables so the same ``TinyEarn`` class can be used across mutliple tickers.



## Examples

The ``Ticker`` module, which allows you to access ticker data in amore Pythonic way:

``` python

    import TinyEarn as ty

    scraper = .tyTinyEarn()
	tsla = scraper.get_earnings('AMZN', start = '04/23/2017', pandas=True, delay=0)
	print(tsla)

	#print(zacky)
	#zacky.info()
	#zacky.describe()

```
```console

                        Period Ending  Estimated_EPS  Reported_EPS  ...  Reported_Revenue  Surprise_Revenue  Surprise_%_Revenue
            2020-04-29    2020-03-01          -0.22          1.24  ...           5985.00            610.13              0.1135
            2020-01-29    2019-12-01           1.62          2.14  ...           7384.00            337.18              0.0478
            2019-10-23    2019-09-01          -0.15          1.86  ...           6303.00           -214.00             -0.0328
            2019-07-24    2019-06-01          -0.54         -1.12  ...           6349.68            -25.81             -0.0040
            2019-04-24    2019-03-01          -1.21         -2.90  ...           4541.46          -1237.27             -0.2141
```

``` python

	#print(zacky)
	#zacky.info()
	#zacky.describe()

```
```console

                        Period Ending  Estimated_EPS  Reported_EPS  ...  Reported_Revenue  Surprise_Revenue  Surprise_%_Revenue
            2020-04-29    2020-03-01          -0.22          1.24  ...           5985.00            610.13              0.1135
            2020-01-29    2019-12-01           1.62          2.14  ...           7384.00            337.18              0.0478
            2019-10-23    2019-09-01          -0.15          1.86  ...           6303.00           -214.00             -0.0328
            2019-07-24    2019-06-01          -0.54         -1.12  ...           6349.68            -25.81             -0.0040
            2019-04-24    2019-03-01          -1.21         -2.90  ...           4541.46          -1237.27             -0.2141
```

sdfa