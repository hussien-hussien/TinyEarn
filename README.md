# TinyEarn - Webscraper for Zacks.com

TinyEarn is an simple selenium-based webscaper to pull earnings data from zacks.com. It navigates to zacks.com/stock/research/{TICKER}/earnings-announcements and scrapes the earnings data from the present table and the table on the sales tab.

Requirements:
* Python3
* Firefox Browser

Packages:
* pandas>=0.24
* numpy>=1.15.4
* selenium>=3.3.0
* requests>=2.23
* beautifulsoup4>=4.9.0

The above packages should auto-install when you install TinyEarn. If you are downloading from github, you should be able to run the following code to install dependencies if you run into any issues.
`` pip install -r requirements.txt ``


## Get Started
Simply install the package using pip in your command line.

``pip install TinyEarn``

## Usage

There is one public function in the ``TinyEarn()`` Class: ``get_earnings()``. It stores no private variables so the same ``TinyEarn()`` class can be used across mutliple tickers.

``get_earnings()``  - Scrapes zacks.com/stock/research/{TICKER}/earnings-announcements to get earnings data. NaN values are filled in for missing data. Dollar values and percentages are expressed as floating point decimals.

Parameters:
* ticker (str): The stock ticker for the company you'd like to pull data for.
* start (datetime.date or str): Only pull data from earnings reported after this date.
* end (datetime.date or str): Only pull data from earnings reported before this date. Defaults to the current date.
* pandas(bool, optional): If true, this function returns a pandas dataframe. If False, it returns a dictionary. Defaults to True.
* delay (int): Time to wait (in seconds) inbetween page changes. Defaults to 1.

Returns:
    Returns data from each earnings report by the specificied company within the specified date range. Each row or key represents an earnings call with the following attributes:
*   `Period Ending`: The month that marks the last month of the quarter being reported on. ie, 3/2017 is refering to the Q1 2017 earnings report.
*   `Reported_EPS`: Earnings Per Share reported by the company for thar quarter.
*   `Estimated_EPS`: The consensus estimated Earnings Per Share.
*   `Surprise_EPS`: The surprise in EPS. The difference between the estimated EPS and the reported one.
*   `Surprise_%_EPS`: The surprise expressed as a percentage.
*   `Reported_Revenue`: Total Revenue reported by the company for that quarter.
*   `Estimated_Revenue`: The consensus estimated Revenue.
*   `Surprise_Revenue`: The surprise in Revenue. The difference between the estimated Revenue and the reported one.
*   `Surprise_%_Revenue`: The surprise expressed as a percentage.
            


## Examples

A few examples of how this class can be used:

``` python
import TinyEarn as ty

scraper = ty.TinyEarn()
tsla = scraper.get_earnings('TSLA', start = '04/23/2017', pandas=True, delay=0) # Get earnings from April 23rd 2017 to today.
tsla[['Period Ending','Estimated_EPS','Reported_EPS','Surprise_EPS','Estimated_Revenue','Reported_Revenue','','']]

```

|            | Period Ending | Estimated_EPS | Reported_EPS | Surprise_EPS | Estimated_Revenue | Reported_Revenue |
|------------|---------------|---------------|--------------|--------------|-------------------|------------------|
| 2020-04-29 | 2020-03-01    | -0.22         | 1.24         | 1.46         | 5374.87           | 5985.00          |
| 2020-01-29 | 2019-12-01    | 1.62          | 2.14         | 0.52         | 7046.82           | 7384.00          |
| 2019-10-23 | 2019-09-01    | -0.15         | 1.86         | 2.01         | 6517.00           | 6303.00          |
| 2019-07-24 | 2019-06-01    | -0.54         | -1.12        | -0.58        | 6375.49           | 6349.68          |
| 2019-04-24 | 2019-03-01    | -1.21         | -2.90        | -1.69        | 5778.73           | 4541.46          |
| 2019-01-30 | 2018-12-01    | 2.08          | 1.93         | -0.15        | 7139.45           | 7225.87          |
| 2018-10-24 | 2018-09-01    | -0.55         | 2.90         | 3.45         | 5666.67           | 6824.41          |
| 2018-08-01 | 2018-06-01    | -2.78         | -3.06        | -0.28        | 3802.96           | 4002.23          |
| 2018-05-02 | 2018-03-01    | -3.37         | -3.35        | 0.02         | 3169.77           | 3408.75          |
| 2018-02-07 | 2017-12-01    | -3.19         | -3.04        | 0.15         | 3298.70           | 3288.25          |
| 2017-11-01 | 2017-09-01    | -2.45         | -2.92        | -0.47        | 2916.96           | 2984.68          |
| 2017-08-02 | 2017-06-01    | -1.94         | -1.33        | 0.61         | 2548.22           | 2789.56          |
| 2017-05-03 | 2017-03-01    | -0.55         | -1.33        | -0.78        | 2561.14           | 2696.27          |





``` python

tsla.info()

```


```console
<class 'pandas.core.frame.DataFrame'>
DatetimeIndex: 13 entries, 2020-04-29 to 2017-05-03
Data columns (total 9 columns):
Period Ending         13 non-null datetime64[ns]
Estimated_EPS         13 non-null float64
Reported_EPS          13 non-null float64
Surprise_EPS          13 non-null float64
Surprise_%_EPS        13 non-null float64
Estimated_Revenue     13 non-null float64
Reported_Revenue      13 non-null float64
Surprise_Revenue      13 non-null float64
Surprise_%_Revenue    13 non-null float64
dtypes: datetime64[ns](1), float64(8)
memory usage: 1.0 KB
                        
```

``` python
import TinyEarn as ty

scraper = ty.TinyEarn()
msft = scraper.get_earnings('MSFT', start = '01/01/2018',end='01/23/2019', delay=0)
msft[['Reported_EPS','Reported_Revenue']]

```
|            | Reported_EPS | Reported_Revenue |
|------------|--------------|------------------|
| 2018-10-24 | 1.14         | 29084.0          |
| 2018-07-19 | 1.13         | 30085.0          |
| 2018-04-26 | 0.95         | 26819.0          |
| 2018-01-31 | 0.96         | 28918.0          |



``` python
import TinyEarn as ty

scraper = ty.TinyEarn()
JPM = scraper.get_earnings('JPM', start = '04/23/2017', pandas=False, delay=0) #Testing Return as Dict
print(JPM)

```


``` console
{Timestamp('2020-04-14 00:00:00'): 
	{'Period Ending': Timestamp('2020-03-01 00:00:00'), 
	'Estimated_EPS': 1.7, 
	'Reported_EPS': 0.78, 
	'Surprise_EPS': -0.92, 
	'Surprise_%_EPS': -0.5412, 
	'Estimated_Revenue': 29152.0, 
	'Reported_Revenue': 28251.0, 
	'Surprise_Revenue': -901.0, 
	'Surprise_%_Revenue': -0.030899999999999997},
Timestamp('2020-01-14 00:00:00'): 
	{'Period Ending': Timestamp('2019-12-01 00:00:00'), 
	'Estimated_EPS': 2.32, 
	'Reported_EPS': 2.57, 
	'Surprise_EPS': 0.25, 
	'Surprise_%_EPS': 0.10779999999999999, 
	'Estimated_Revenue': 27261.0, 
	'Reported_Revenue': 28331.0, 
	'Surprise_Revenue': 1070.0, 
	'Surprise_%_Revenue': 0.0393}, 
Timestamp('2019-10-15 00:00:00'): 
	{'Period Ending': Timestamp('2019-09-01 00:00:00'), 
	'Estimated_EPS': 2.44, 
	'Reported_EPS': 2.68, 
	'Surprise_EPS': 0.24, 
	'Surprise_%_EPS': 0.0984, 
	'Estimated_Revenue': 28403.0, 
	'Reported_Revenue': 29341.0, 
	'Surprise_Revenue': 938.0, 
	'Surprise_%_Revenue': 0.033}, 
Timestamp('2019-07-16 00:00:00'): 
	{'Period Ending': Timestamp('2019-06-01 00:00:00'), 
	'Estimated_EPS': 2.5, 
	'Reported_EPS': 2.59, 
	'Surprise_EPS': 0.09, 
	'Surprise_%_EPS': 0.036000000000000004, 
	'Estimated_Revenue': 28416.5, 
	'Reported_Revenue': 28832.0, 
	'Surprise_Revenue': 415.5, 
	'Surprise_%_Revenue': 0.0146}}

```






