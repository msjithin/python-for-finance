
from os import write
from PIL import Image
import streamlit as st 
import datetime as dt
import matplotlib.pyplot as plt
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from stock_analysis import *
from streamlit.elements import button
# Use the full page instead of a narrow central column
st.set_page_config(page_title='Stock web app')

image1, image2, image3 = st.beta_columns([2,1,1])
#Add title and image 
image1.write("""
# Stock Market Analysis
""")
top_image = Image.open('assets/stockimage.jpg')
image2.image(top_image, use_column_width=True)

#Create site bar header
st.sidebar.header('User Input')
#add select widget
st.sidebar.subheader('Select Stock')
stock_names = ['Microsoft', 'Apple', 'S&P 500']
dropdown_select_stock = st.sidebar.selectbox(label='Stock name', options=stock_names)
stock_selected = 'MSFT'
if dropdown_select_stock == 'Microsoft':
    stock_selected = 'MSFT'
elif dropdown_select_stock == 'Apple':
    stock_selected = 'AAPL'
elif dropdown_select_stock == 's&P 500':
    stock_selected = '^GSPC'
st.write(get_time_series(stock_selected))

st.subheader('Log returns')
st.write(plot_return())

def weights_pie_chart():
    #pie chart for weights
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = stock_names
    sizes = [1/3, 1/3, 1/3]
    print(labels)
    print(sizes)
    explode = (0, 0.1, 0, )  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    return fig1

st.subheader('Weights')    
st.write(weights_pie_chart())

st.subheader('Portfolio returns')
st.write(portfolio_returns())

st.sidebar.write('**Total portfolio return is** : ' )
st.sidebar.success('{:5.2f}'.format(100 * total_portfolio_return) + '%')
st.sidebar.write('**Average yearly return is**  : ' )
st.sidebar.success('{:5.2f}'.format(100 * average_yearly_return) + '%')

st.subheader('Price')
st.write(plot_price(stock_selected))

st.subheader('EMA')
st.write(plot_ema(stock_selected))

st.subheader('Trading position')
st.write(plot_trading_position(stock_selected))

st.subheader('Best return ')
st.write(plot_best_returns())

st.subheader('Total returns ')
st.write(total_retuns())

print(dt.datetime.now().strftime("%H:%M:%S") , ' script end reached .....')