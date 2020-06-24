import pandas as pd
import numpy as np
import math
import datetime
import time
import requests
import json
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from collections import defaultdict
import statsmodels.api as sm
from bs4 import BeautifulSoup
import datetime
import re


class TinyEarn():
    ''' 
    This class scrapes Zacks.com to get earnings data from a companies earnings reports.
    '''

    def get_earnings(self, ticker:str, start, end = datetime.date.today(), pandas = True, delay = 1):
        """Scrapes zacks.com/stock/research/{TICKER}/earnings-announcements to get earnings data.

        Args:
            ticker (str): The stock ticker for the company you'd like to pull data for.
            start (datetime.date or str): Only pull data from earnings reported after this date.
            end (datetime.date or str): Only pull data from earnings reported before this date. Defaults to the current date.
            pandas(bool, optional): If true, this function returns a pandas dataframe. If False, it returns a dictionary. Defaults to True.
            delay (int): Time to wait (in seconds) inbetween page changes. Defaults to 1.

        Returns:
            Returns data from each earnings report by the specificied company within the specified date range. Each row or key represents an earnings call with the following attributes:
                `Period Ending`: The month that marks the last month of the quarter being reported on. ie, 3/2017 is refering to the Q1 2017 earnings report.
                `Reported_EPS`: Earnings Per Share reported by the company for thar quarter.
                `Estimated_EPS`: The consensus estimated Earnings Per Share.
                `Surprise_EPS`: The surprise in EPS. The difference between the estimated EPS and the reported one.
                `Surprise_%_EPS`: The surprise expressed as a percentage.
                `Reported_Revenue`: Total Revenue reported by the company for that quarter.
                `Estimated_Revenue`: The consensus estimated Revenue.
                `Surprise_Revenue`: The surprise in Revenue. The difference between the estimated Revenue and the reported one.
                `Surprise_%_Revenue`: The surprise expressed as a percentage.
            NaN values are filled in for missing data and percentages are expressed as floating point decimals.

        Examples:
            >>> scraper = TinyEarn()
            >>> tsla = scraper.get_earnings('TSLA', start = '04/23/2019', pandas=True, delay=0)
            >>> print(tsla)
                        Period Ending  Estimated_EPS  Reported_EPS  ...  Reported_Revenue  Surprise_Revenue  Surprise_%_Revenue
            2020-04-29    2020-03-01          -0.22          1.24  ...           5985.00            610.13              0.1135
            2020-01-29    2019-12-01           1.62          2.14  ...           7384.00            337.18              0.0478
            2019-10-23    2019-09-01          -0.15          1.86  ...           6303.00           -214.00             -0.0328
            2019-07-24    2019-06-01          -0.54         -1.12  ...           6349.68            -25.81             -0.0040
            2019-04-24    2019-03-01          -1.21         -2.90  ...           4541.46          -1237.27             -0.2141
            >>> 
            
        """
        
        # Check to make sure date times are correct types, 
        # if either are strings try to convert them to datetime objects
        if isinstance(start,str): start = pd.to_datetime(start)
        if isinstance(end,str): end = pd.to_datetime(end)

        # Raises error if either end or start was an invalid input
        if not isinstance(start, datetime.date) or not isinstance(end, datetime.date):
            raise ValueError('Type error occured with start or end parameters. Please enter valid date string or datetime object.')

        # Start firefox browser in selenium
        browser = self.__get_browser()

        # Open zacks.com 
        url = "https://www.zacks.com/stock/research/" + ticker + "/earnings-announcements"
        browser.get(url)

        # Passess browser into get earnings, returns earnings table
        eps = self.__get_eps(browser, start,end,url,delay)

        # passess same browser into get_revenue, returns revenue table
        revenue = self.__get_revenue(browser, start,end,url,delay)

        # Close browser and process results for output
        browser.close()

        # Run sequence to merge those eps and revenue dictionaries by earnings report
        results = self.__merge_dicts(eps,revenue)

        # Depending on params, return dataframe or dictionary
        if pandas == True:
            return pd.DataFrame.from_dict(results, orient='index')
        else:
            return results


    def __merge_dicts(self, first:dict, second:dict):
        """This helper function merges two two-level dictionaries together on common keys. 
        Error will be raised if there aren't the same unique keys in each dictionary.

        Args:
            first: First dictionary
            second: Second dictionary

        Returns:
            One dictionary with same keys from each dictionary and the values of each dictionary

        """
        for date in first.keys():
            first[date].update(second[date])
        return first

    def __clean_vals(self, value:str):
        """
        Takes in string value, cleans it of non float characters ('%','$',',') and returns it as a float. 
        If value is empty according to Zacks.com conventions then we just return a 0.
        """
        if value == '--':
            return np.nan
        else:
            return float(value.replace('$',"").replace('%',"").replace(',',''))

    def __get_eps(self, browser, start, end, url, delay = 1):
        """
        Performs operations to scrape data related to Earnings Per Share (EPS) from zacks.com/stock/research/{TICKER}/earnings-announcements
        """

        # Declare variables
        stats_list = {}
        return_list = {}
        done = False

        # This loop iterates through each row, pulls data from each column then moves onto the next page to continue if neccessary
        # done represents whether we have reached the date in earnings report that we want to stop scraping
        while done == False:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Try to find earnings table
            # If it cannot be found then the ticker probably is not reported on by zacks.com and we are looking at a searching results screen
            try:
                table = soup.find_all('table', id='earnings_announcements_earnings_table')[0].find('tbody')
            except IndexError:
                error = "Encountered an error trying to access "+url+". The ticker you specified may not be available on Zacks.com."
                raise KeyError(error) from None

            # Create a list of all rows present on the screen
            rows = table.find_all('tr', attrs={'role':'row'})
            
            # Iterate through each row of earnings reports and pull date from each column
            for row in rows:

                # Pull results from each column
                col = row.find_all('td')
                date = pd.to_datetime(col[0].get_text())

                # If we've reached a row that represents an earnings call that is withing our specified dates of inquiry then clean values and store them in return list
                # Otherwise skip this row or, if we have eached beyond latest date we want to pull then terminate loop and return results
                if date < start:
                    done = True
                    break

                elif date < end:
                    stats_list['Period Ending'] = pd.to_datetime(col[1].get_text()) # Period Ending
                    stats_list['Estimated_EPS'] = self.__clean_vals(col[2].get_text()) # Estimated EPS
                    stats_list['Reported_EPS'] = self.__clean_vals(col[3].get_text()) # Reported EPS
                    stats_list['Surprise_EPS'] = self.__clean_vals(col[4].get_text()) # Surprise
                    stats_list['Surprise_%_EPS'] = (self.__clean_vals(col[5].get_text()) / 100) # Surprise %
                    #stats_list['Ticker'] = ticker 
                    return_list[date] = stats_list
                
                stats_list = {}

            # Find next page button
            next_btn = browser.find_element_by_xpath('//*[@id="earnings_announcements_earnings_table_next"]')
            location = next_btn.location
            
            # Scroll next page button into view
            y = location['y'] - 100
            browser.execute_script("window.scrollTo(0, " + str(y) + ")") 
            time.sleep(delay)
            
            # Click on next page button
            actions = ActionChains(browser)
            actions.move_to_element(next_btn)
            actions.click(next_btn)
            actions.perform()

        return return_list

    def __get_revenue(self, browser, start, end, url, delay = 1):
        """
        Performs operations to scrape data related to Revenue from zacks.com/stock/research/{TICKER}/earnings-announcements
        """
        done = False
        stats_list = {}
        return_list = {}

        # Navigate to Sales Tab
        sales_btn = browser.find_element_by_xpath('//*[@id="ui-id-4"]')
        sales_loc = sales_btn.location
            
        # Scroll next button into view
        y = sales_loc['y'] - 100
        browser.execute_script("window.scrollTo(0, " + str(y) + ")") 

        # Click on sales tab button
        actions = ActionChains(browser)
        actions.move_to_element(sales_btn)
        actions.click(sales_btn)
        actions.perform()

        # This loop pulls data from each row then moves onto the next page to continue if neccessary
        # done represents whether we have reached the date in earnings report that we want to stop scraping
        while done == False:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Try to find sales table
            # If it cannot be found then the ticker probably is not reported on by zacks.com and we are looking at a searching results screen
            try:
                table = soup.find_all('table', id='earnings_announcements_sales_table')[0].find('tbody')
            except IndexError:
                error = "Encountered an error trying to access "+url+". The ticker you specified may not be available on Zacks.com."
                raise Exception(error)

            # Create a list of all rows present on the screen
            rows = table.find_all('tr', attrs={'role':'row'})
            
            # This loop iterates through each row, pulls data from each column then moves onto the next page to continue if neccessary
            # done represents whether we have reached the date in earnings report that we want to stop scraping
            for row in rows:
                # Pull results from each column
                col = row.find_all('td')
                date = pd.to_datetime(col[0].get_text())

                # If we've reached a row that represents an earnings call that is withing our specified dates of inquiry then clean values and store them in return list
                # Otherwise skip this row or, if we have eached beyond latest date we want to pull then terminate loop and return results
                if date < start:
                    done = True
                    break

                elif date < end:
                    stats_list['Period Ending'] = pd.to_datetime(col[1].get_text()) # Period Ending
                    stats_list['Estimated_Revenue'] = self.__clean_vals(col[2].get_text()) # Estimated EPS
                    stats_list['Reported_Revenue'] = self.__clean_vals(col[3].get_text()) # Reported EPS
                    stats_list['Surprise_Revenue'] = self.__clean_vals(col[4].get_text()) # Surprise
                    stats_list['Surprise_%_Revenue'] = (self.__clean_vals(col[5].get_text()) / 100) # Surprise %
                    return_list[date] = stats_list
                
                stats_list = {}

            # Find next page button
            next_btn = browser.find_element_by_xpath('//*[@id="earnings_announcements_sales_table_next"]')
            location = next_btn.location
            
            # Scroll next button into view
            y = location['y'] - 100
            browser.execute_script("window.scrollTo(0, " + str(y) + ")") 
            time.sleep(delay)
            
            # Click on it
            actions = ActionChains(browser)
            actions.move_to_element(next_btn)
            actions.click(next_btn)
            actions.perform()

        return return_list

    
    def __get_browser(self):
        ''' Initiate and return firefox browser using gecko driver.
        '''
        opts = Options()
        opts.headless = True
        browser = Firefox(executable_path=r'./geckodriver',
                          options=opts)
        return browser


scraper = TinyEarn()
tsla = scraper.get_earnings('AMZN', start = '04/23/2017', pandas=True, delay=0)
print(tsla)

#print(zacky)
#zacky.info()
#zacky.describe()