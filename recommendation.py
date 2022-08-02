import streamlit as st
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime
import random

def app():
    def specific_string(length):
        sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'  # define the specific string
        # define the condition for random string
        result = ''.join((random.choice(sample_string)) for x in range(length))
        return result

    def load_ticker_data(page_type):
        st.write('---')
        # Sidebar

        start_date = st.date_input("Start date", datetime.date(2019, 1, 1), key=specific_string(5))
        end_date = st.date_input("End date", datetime.date(2021, 1, 31), key=specific_string(5))

        ticker_list = pd.read_csv(
            'https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
        tickerSymbol = ticker_list["ABT"][
            random.randint(-1, len(ticker_list["ABT"]))]  # each time it will pick random from list
        tickerData = yf.Ticker(tickerSymbol)  # Get ticker data
        tickerDf = tickerData.history(period='1d', start=start_date,
                                      end=end_date)  # get the historical prices for this ticker

        string_logo = '<img src=%s>' % tickerData.info['logo_url']
        st.markdown(string_logo, unsafe_allow_html=True)

        string_name = tickerData.info['longName']
        st.header('**%s**' % string_name)

        string_summary = tickerData.info['longBusinessSummary']
        st.info(string_summary)

        # Ticker data
        st.header('**Ticker data**')
        st.write(tickerDf)

        st.write('---')

    def main_page():

        # App title
        st.markdown('''
      # Stock Price App
      ''')
        st.write('---')

        # Sidebar

        start_date = st.date_input("Start date", datetime.date(2019, 1, 1), key=specific_string(5))
        end_date = st.date_input("End date", datetime.date(2021, 1, 31), key=specific_string(5))

        # Retrieving tickers data
        ticker_list = pd.read_csv(
            'https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
        tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list, key=specific_string(5))  # Select ticker symbol

        tickerData = yf.Ticker(tickerSymbol)  # Get ticker data
        tickerDf = tickerData.history(period='1d', start=start_date,
                                      end=end_date)  # get the historical prices for this ticker

        string_logo = '<img src=%s>' % tickerData.info['logo_url']
        st.markdown(string_logo, unsafe_allow_html=True)

        string_name = tickerData.info['longName']
        st.header('**%s**' % string_name)

        string_summary = tickerData.info['longBusinessSummary']
        st.info(string_summary)

        # Ticker data
        st.header('**Ticker data**')
        st.write(tickerDf)

        # Bollinger bands
        st.header('**Bollinger Bands**')
        qf = cf.QuantFig(tickerDf, title='First Quant Figure', legend='top', name='GS')
        qf.add_bollinger_bands()
        fig = qf.iplot(asFigure=True)
        st.plotly_chart(fig)

    def page_recommend_to_buy():
        st.header('**Recommened to Buy**')
        load_ticker_data("buy")
        if st.button("Return to Main Page"):
            st.session_state.runpage = main_page
            st.experimental_rerun()

    def page_recommend_to_sell():
        st.header('**Recommened to Sell**')
        load_ticker_data("sell")
        if st.button("Return to Main Page"):
            st.session_state.runpage = main_page
            st.experimental_rerun()

    buy_btn = st.button("Recommend to Buy")
    sell_btn = st.button("Recommend to Sell")

    if buy_btn:
        st.session_state.runpage = page_recommend_to_buy
        st.session_state.runpage()
    elif sell_btn:
        st.session_state.runpage = page_recommend_to_sell
        st.session_state.runpage()
    else:
        main_page()
