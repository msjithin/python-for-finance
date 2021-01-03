

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from pathlib import Path

style.use('ggplot')
print(""" 
Functions : 
            get_csv(stock_name = 'stock', start_year=2000, end_year=2020)  --> retrieve stock info
            read_csv(stock_name):                                          --> plot stock info

""")
def get_csv(stock_name = 'stock', start_year=2000, end_year=2020):
    ''' 
    Function to retrieve stock info
    arguments:
       stock_name : str
       start_year : int
       end_year   : int
    '''
    start = dt.datetime(start_year, 1, 1)
    end = dt.datetime(end_year, 12, 31)
    df = web.DataReader(str(stock_name), 'yahoo', start, end)
    df.to_csv(stock_name.lower()+'.csv')

def read_csv(stock_name):
    '''
    Function to read and plot stock info
    arguments:
       stock_name : str
    '''
    file_name = stock_name.lower()+'.csv'
    if not Path(file_name).exists():
        print("Data didn't exist, getting stock data")
        get_csv(stock_name)
    else:
        print("Data exists ..........  ")
    df = pd.read_csv( file_name, parse_dates = True, index_col = 0)
    print(df.head())
    df['Adj Close'].plot()
    plt.show()


#get_csv('TSLA', end_year=2020)
#read_csv('tsla.csv')
