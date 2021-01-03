#Description : This is a stock market dashboard 
# to show some charts and data and stocks

import pandas as pd 
from PIL import Image
import streamlit as st 
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from pathlib import Path
import json

#Add title and image 
st.write("""
# Stock Market Web Application
**Visually** show  data on a stock! Data range from Jan, 2000
""")

image = Image.open('assets/stockimage.jpg')
st.image(image, use_column_width=True)

#Create site bar header
st.sidebar.header('User Input')

#get stock data
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
    df.to_csv('data/'+stock_name.lower()+'.csv')

#Create function to get user input
def get_input():
    start_date = st.sidebar.text_input("Start Date", "2010-01-02")
    end_date = st.sidebar.text_input("End Date", "2020-12-31")
    stock_symbol = st.sidebar.text_input("Stock symbol", "aapl")
    company = st.sidebar.text_input("Company", "Apple")
    return start_date, end_date, stock_symbol.lower(), company

#Create a function to get company name
def get_company_name(symbol):
    with open('data/nasdaq-listed-symbols_json.json') as jsfile:
        data = json.load(jsfile)
        for p in data:
            if symbol.upper() == p['Symbol']:
                return p['Company Name']
    with open('data/nyse-listed_json.json') as jsfile:
        data = json.load(jsfile)
        for p in data:
            if symbol.upper() == p['ACT Symbol']:
                return p['Company Name']
    return symbol

#Create function to get dataset
def  get_data(symbol, start, end):
    file_name = 'data/'+symbol.lower()+'.csv'
    print('Looking for data for '+symbol)
    if not Path(file_name).exists():
        print("Data didn't exist, getting stock data")
        get_csv(symbol)
    else:
        print("Data exists ..........  ")
    #load data
    df = pd.read_csv('data/'+symbol+".csv")
    #get date range
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    
    #set start and end rows to 0
    start_row = 0
    end_row = 0
    #start date from top/first line of dataset
    for i in range(0, len(df)):
        if start <= pd.to_datetime( df['Date'][i] ):
            start_row = i
            break 
    #end date from last line of dataset
    for j in range(len(df)):
        if end >= pd.to_datetime( df['Date'][len(df)-1-j] ):
            end_row = len(df) - 1 -j
            break
    #set index to date
    df = df.set_index(pd.DatetimeIndex(df['Date'].values))
    return df.iloc[start_row:end_row+1, :]


#get user input
start, end, symbol, company = get_input()
#get data
df = get_data(symbol, start, end)
#get company name
company_name = get_company_name(symbol)

#Display the close price
st.header(company_name+' Close price \n')
st.line_chart(df['Close'])

#Display the volume price
st.header(company_name+' Volume \n')
st.line_chart(df['Volume'])

#get statistics
st.header('Data statistics')
st.write(df.describe())
print('Everything ran ..... ')




