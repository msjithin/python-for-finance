
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