######################################################################
#
# WEB SCRAPING DEPOSIT RATES
# (top 40 banks by product)
#
######################################################################

"""
SOURCE:   depositaccounts.com (by LendingTree)
AUTHOR:   Gerard Mazi
CONTACT:  gerard.mazi@gmail.com
"""

import pandas as pd
from scrapy import Selector
import requests
from datetime import date

# Target URL's containing all deposit rates
url = ['https://www.depositaccounts.com/cd/3-month-cd-rates.html',
       'https://www.depositaccounts.com/cd/6-month-cd-rates.html',
       'https://www.depositaccounts.com/cd/',
       'https://www.depositaccounts.com/cd/18-month-cd-rates.html',
       'https://www.depositaccounts.com/cd/2-year-cd-rates.html',
       'https://www.depositaccounts.com/cd/3-year-cd-rates.html',
       'https://www.depositaccounts.com/cd/4-year-cd-rates.html',
       'https://www.depositaccounts.com/cd/5-year-cd-rates.html',
       'https://www.depositaccounts.com/savings/',
       'https://www.depositaccounts.com/moneymarket/']

# Flag for deposit product or CD term if Cd
product = ['3 Month', '6 Month', '12 Month','18 Month',
           '24 Month', '36 Month','48 Month','60 Month',
           'Savings','Money Market']

# Merge URL's and Products
lookup = pd.DataFrame({"URL":url, "Product":product})

# Create empty DataFrame to be filled in by loop
todays_rates = pd.DataFrame(
        {"Bank":[], "Product_Name":[], "Rate":[], "URL":[]}
        )

# Loop through all the sites
for u in lookup['URL'].tolist():
    html = requests.get(u).content
    sel = Selector(text = html)
    
    banks = sel.xpath('//div[@class = "bank"]/a[1]/text()').extract()
    rates = sel.xpath('//div[@class = "apy"]/span/text()').extract()
    prod = sel.xpath('//div[@class = "bank"]/span/text()').extract()
    url = u
    
    rates_int = pd.DataFrame(
            {"Bank":banks, 
             "Product_Name":prod, 
             "Rate":rates, 
             "URL":url}
            )
    
    todays_rates = pd.concat(
            [todays_rates, rates_int],
            ignore_index = True
            )

# Cleanup: Add Date, Add Product Type, Coerce rate to float    
todays_rates["Date"] = date.today()
todays_rates = pd.merge(todays_rates, lookup, on='URL',how='left')
todays_rates['Rate'] = todays_rates['Rate'].str.rstrip('%').astype('float')

# load running file
# append todays_rates and save for ongoing data collection