#Description : This program attempts to optimize user portfolio using Efficinet Frontier

#import libraries
from pandas_datareader import data as web
import pandas as pd 
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


#get stock symbols/tickers in portfolio
#FAANG
assets = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOG']

#assign weights to the stocks
weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

#get stock/portfolio start and end date
stock_start_date = '2013-01-01'
stock_end_date = today = datetime.today().strftime('%Y-%m-%d')

#create dataframe to store adjusted close price
df = pd.DataFrame()

#store adj close price
for stock in assets:
    df[stock] = web.DataReader(stock, data_source='yahoo', start=stock_start_date, end=stock_end_date)['Adj Close']

#visually show stock/portfolio
title = 'Portfolio Adj. Close price history'
my_stocks = df

#create and plot grph
for c in my_stocks.columns.values:
    plt.plot(my_stocks[c], label=c)

plt.title(title)
plt.xlabel('Date', fontsize = 18)
plt.ylabel('Adj. Price USD ($)', fontsize = 18)
plt.legend(my_stocks.columns.values, loc='upper left')
#plt.show()

#show daily simple return 
returns = df.pct_change()

#create and show anualized covariance matrix
cov_matrix_annual = returns.cov() * 252

#calculate the portfolio variance
port_variance = np.dot(weights.T, np.dot(cov_matrix_annual, weights))
#print(port_variance)

#calculate portfolio volatility aks std deviation
port_volatility = np.sqrt(port_variance)

#calculate annual portfolio returns
portfolio_simple_annual_return = np.sum(returns.mean() * weights) * 252
#print(portfolio_simple_annual_return)

#show expected annual return, volatility (aka risk) and variance
percent_var = str(round(port_variance, 2)*100) + '%'
percent_vols = str(round(port_volatility, 2)*100) + '%'
percent_ret = str(round(portfolio_simple_annual_return, 2)*100) + '%'

print('Expected annual return: '+ percent_ret)
print('Annual volatility / risk: '+ percent_vols)
print('Annual variance : '+ percent_var)

from pypfopt.efficient_frontier import EfficientFrontier







