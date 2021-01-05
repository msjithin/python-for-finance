#Description : This is a stock market dashboard 
# to show some charts and data and stocks

from os import write
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
#import plotly.express as px
from streamlit.elements import button
# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

image1, image2, image3 = st.beta_columns([2,1,1])
#Add title and image 
image1.write("""
# Stock Market Web Application
**Visually** show  data on a stock! Data range from Jan, 2000
""")
image = Image.open('assets/stockimage.jpg')
image2.image(image, use_column_width=True)

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
    #company = st.sidebar.text_input("Company", "Apple")
    return start_date, end_date, stock_symbol.lower()

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
start, end, symbol = get_input()
#get data
df = get_data(symbol, start, end)
#get company name
company_name = get_company_name(symbol)
company = st.sidebar.text_input("Company", company_name)
# For radio box selection - select time range using radio box
# st.sidebar.subheader('Select Date range')
# radio_button = st.sidebar.radio('Choose date range', 
#     options=['All', 'Last 5 years', 'Last 1 year', 'Last 3 months'])
#Display the close price
# st.header(company_name+' Close price \n')
# if radio_button == 'All':
#     st.line_chart(df['Close'])
# elif radio_button == 'Last 3 months':
#     df = df.last('3M')
#     st.line_chart(df['Close'])
# elif radio_button == 'Last 1 year':
#     df = df.last('1Y')
#     st.line_chart(df['Close'])
# elif radio_button == 'Last 5 years':
#     df = df.last('5Y')
#     st.line_chart(df['Close'])

# select  time using buttons on top of chart
st.subheader('Choose date range for chart')
button1, button2, button3, button4 = st.beta_columns(4)
b1 = button1.button('      All    ')
b2 = button2.button('Last 5 years ')
b3 = button3.button(' Last 1 year ')
b4 = button4.button('Last 3 months')

#Display the close price
st.header(company_name+' Close price \n')
if b1:
    st.line_chart(df['Close'])
elif b4:
    df = df.last('3M')
    st.line_chart(df['Close'])
elif b3:
    df = df.last('1Y')
    st.line_chart(df['Close'])
elif b2:
    df = df.last('5Y')
    st.line_chart(df['Close'])
else:
    st.line_chart(df['Close'])

#add select widget
st.sidebar.subheader('Select plot for second chart range')
x_options = ['Date','High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close']
y_options = ['Volume', 'High', 'Low', 'Open', 'Close', 'Adj Close']
dropdown_select1 = st.sidebar.selectbox(label='X axis', options=x_options)
dropdown_select2 = st.sidebar.selectbox(label='Y axis', options=y_options)
st.header(company_name+' '+dropdown_select2+'\n')
if dropdown_select1 == 'Date':
    st.line_chart(df[dropdown_select2])
else:
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.scatter(
        df[dropdown_select1],
        df[dropdown_select2],
    )
    ax.set_xlabel(dropdown_select1)
    ax.set_ylabel(dropdown_select2)
    st.write(fig)

# checkbox widget
checkbox_stat = st.sidebar.checkbox('Reveal data statistics')
if checkbox_stat:
    #get statistics
    st.header('Data statistics')
    st.write(df.describe())
# checkbox widget for statistics
checkbox = st.sidebar.checkbox('Reveal data ')
if checkbox:
    #write data to page
    st.header('Data')
    #st.write(df)
    st.dataframe(data=df)


print('Everything ran ..... ')
