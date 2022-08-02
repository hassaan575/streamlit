import streamlit as st
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime
from sklearn.svm import SVR


# App title
def app():
    st.title('Stock Data')



# Sidebar
    st.sidebar.subheader('Select Date')
    start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
    end_date = st.sidebar.date_input("End date", datetime.date(2021, 1, 31))

# Retrieving tickers data
    ticker_list = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv')
    tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list) # Select stock symbol
    tickerData = yf.Ticker(tickerSymbol) # Get stock data
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this stock

    Favlist = st.sidebar.selectbox('Favorite List', ticker_list)
# stock logo and summary
    string_logo = '<img src=%s>' % tickerData.info['logo_url']
    st.markdown(string_logo, unsafe_allow_html=True)

    string_name = tickerData.info['longName']
    st.header('**%s**' % string_name)

    string_summary = tickerData.info['longBusinessSummary']
    st.info(string_summary)

# stock data
    st.header('**Stock Data**')
    st.write(tickerDf)

# rsi, ema, sma
    st.header('**Stock Chart**')
    qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')

    qf.add_ema(periods=100, color='red')
    qf.add_sma(periods=50, color='blue')
    qf.add_rsi(periods=20, color='black')

    fig = qf.iplot(asFigure=True)
    st.plotly_chart(fig)

####
#st.write('---')
#st.write(tickerData.info)


