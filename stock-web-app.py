#Description : This is a stock market dashboard 
# to show some charts and data and stocks

from os import write
import pandas as pd 
from PIL import Image
import streamlit as st 
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.dates import date2num
import pandas as pd
import pandas_datareader.data as web
from pathlib import Path
import json
import plotly.express as px
import plotly.graph_objects as go

from streamlit.elements import button
# Use the full page instead of a narrow central column
st.set_page_config(page_title='Stock web app', layout="wide")

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
    #end = dt.datetime(end_year, 12, 31)
    end = dt.date.today()
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
                return p['Company Name'], 'NASDAQ'
    with open('data/nyse-listed_json.json') as jsfile:
        data = json.load(jsfile)
        for p in data:
            if symbol.upper() == p['ACT Symbol']:
                return p['Company Name'], 'NYSE'
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
company_name, listed_at = get_company_name(symbol)
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
st.subheader(listed_at + ': '+symbol.upper())
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
    p = plt.axvspan(0, 0.5, facecolor='y', alpha=0.5,zorder=3)
    st.line_chart(df['Close'])

c1, c2, c3 = st.beta_columns([1,2,1])
#add select widget
st.sidebar.subheader('Select plot for second chart range')
x_options = ['Date','High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close']
y_options = ['Volume', 'High', 'Low', 'Open', 'Close', 'Adj Close']
dropdown_select1 = st.sidebar.selectbox(label='X axis', options=x_options)
dropdown_select2 = st.sidebar.selectbox(label='Y axis', options=y_options)
c2.header(company_name+' '+dropdown_select2+'\n')
if dropdown_select1 == 'Date':
    c2.line_chart(df[dropdown_select2])
else:
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.scatter(
        df[dropdown_select1],
        df[dropdown_select2],
    )
    ax.set_xlabel(dropdown_select1)
    ax.set_ylabel(dropdown_select2)
    c2.write(fig)

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




fig = px.line(df['Close'], width=1150, height=500)
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
st.write(fig)



fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
fig.update_layout(
    title='Candlestick graph',
    yaxis_title='AAPL Stock',
    width=1150,
    height=500,
    shapes = [dict(
        x0='2016-12-09', x1='2016-12-09', y0=0, y1=1, xref='x', yref='paper',
        line_width=2)],
    annotations=[dict(
        x='2016-12-09', y=0.05, xref='x', yref='paper',
        showarrow=False, xanchor='left', text='Increase Period Begins')]
)
st.write(fig)




print('Everything ran ..... ')
