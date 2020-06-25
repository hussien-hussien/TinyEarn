import TinyEarn as ty

scraper = ty.TinyEarn()
tsla = scraper.get_earnings('TSLA', start = '04/23/2017', pandas=True, delay=0) # Get earnings from April 23rd 2017 to today.
tsla
