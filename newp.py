import streamlit as st
import time
from tqdm.notebook import tqdm
from tensorflow import keras
import datetime as dt
from datetime import date
import yfinance as yf
import pandas as pd
from plotly import graph_objs as go
import plotly.express as px
import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
from sklearn.svm import SVR
import quandl
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def app():

    START = "2018-01-01"
    TODAY = dt.datetime.now().strftime("%Y-%m-%d")

    st.title("Stock Prediction App")

    n_years = st.slider('Years of prediction:', 1, 4)
    period = n_years * 365

    stocks = ["Select the Stock", "AAPL", "GOOG", "MSFT", "AMZN", "TSLA", "GME", "NVDA", "AMD"]

    # Loading Data ---------------------

    # @st.cache(suppress_st_warning=True)
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data


    # For Stock Financials ----------------------

    # Plotting Raw Data ---------------------------------------

    # For LSTM MOdel ------------------------------

    def create_train_test_LSTM(df, epoch, b_s, ticker_name):

        df_filtered = df.filter(['Close'])
        dataset = df_filtered.values

        # Training Data
        training_data_len = math.ceil(len(dataset) * .7)

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)

        train_data = scaled_data[0: training_data_len, :]

        x_train_data, y_train_data = [], []

        for i in range(60, len(train_data)):
            x_train_data.append(train_data[i - 60:i, 0])
            y_train_data.append(train_data[i, 0])

        x_train_data, y_train_data = np.array(x_train_data), np.array(y_train_data)

        x_train_data = np.reshape(x_train_data, (x_train_data.shape[0], x_train_data.shape[1], 1))

        # Testing Data
        test_data = scaled_data[training_data_len - 60:, :]

        x_test_data = []
        y_test_data = dataset[training_data_len:, :]

        for j in range(60, len(test_data)):
            x_test_data.append(test_data[j - 60:j, 0])

        x_test_data = np.array(x_test_data)

        x_test_data = np.reshape(x_test_data, (x_test_data.shape[0], x_test_data.shape[1], 1))

        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train_data.shape[1], 1)))
        model.add(LSTM(units=50, return_sequences=False))

        model.add(Dense(25))
        model.add(Dense(1))

        model.compile(optimizer='adam', loss='mean_squared_error')

        model.fit(x_train_data, y_train_data, batch_size=int(b_s), epochs=int(epoch))
        st.success("Your Model is Trained Succesfully!")
        st.markdown('')
        st.write("Predicted vs Actual Results for LSTM")
        st.write("Stock Prediction on Test Data for - ", ticker_name)

        predictions = model.predict(x_test_data)
        predictions = scaler.inverse_transform(predictions)

        train = df_filtered[:training_data_len]
        valid = df_filtered[training_data_len:]
        valid['Predictions'] = predictions

        new_valid = valid.reset_index()
        new_valid.drop('index', inplace=True, axis=1)
        st.dataframe(new_valid)
        st.markdown('')
        st.write("Plotting Actual vs Predicted ")

        st.set_option('deprecation.showPyplotGlobalUse', False)
        plt.figure(figsize=(14, 8))
        plt.title('Actual Close prices vs Predicted Using LSTM Model', fontsize=20)
        plt.plot(valid[['Close', 'Predictions']])
        plt.legend(['Actual', 'Predictions'], loc='upper left', prop={"size": 20})
        st.pyplot()

    # Creating Training and Testing Data for other Models ----------------------

    def create_train_test_data(df1):

        data = df1.sort_index(ascending=True, axis=0)
        new_data = pd.DataFrame(index=range(0, len(df1)), columns=['Date', 'High', 'Low', 'Open', 'Volume', 'Close'])

        for i in range(0, len(data)):
            new_data['Date'][i] = data['Date'][i]
            new_data['High'][i] = data['High'][i]
            new_data['Low'][i] = data['Low'][i]
            new_data['Open'][i] = data['Open'][i]
            new_data['Volume'][i] = data['Volume'][i]
            new_data['Close'][i] = data['Close'][i]

        # Removing the hour, minute and second
        new_data['Date'] = pd.to_datetime(new_data['Date']).dt.date

        train_data_len = math.ceil(len(new_data) * .8)

        train_data = new_data[:train_data_len]
        test_data = new_data[train_data_len:]

        return train_data, test_data

    # Finding Movinf Average ---------------------------------------

    # Finding Linear Regression ----------------------------

    def Linear_Regression_model(train_data, test_data):

        x_train = train_data.drop(columns=['Date', 'Close'], axis=1)
        x_test = test_data.drop(columns=['Date', 'Close'], axis=1)
        y_train = train_data['Close']
        y_test = test_data['Close']

        # First Create the LinearRegression object and then fit it into the model
        from sklearn.linear_model import LinearRegression

        model = LinearRegression()
        model.fit(x_train, y_train)

        # Making the Predictions
        prediction = model.predict(x_test)

        return prediction



    # Plotting the Predictions -------------------------

    def prediction_plot(pred_data, test_data, models, ticker_name):

        test_data['Predicted'] = 0
        test_data['Predicted'] = pred_data

        # Resetting the index

        test_data.reset_index(inplace=True, drop=True)
        st.success("Your Model is Trained Succesfully!")
        st.markdown('')
        st.write("Predicted Price vs Actual Close Price Results for - ", models)
        st.write("Stock Prediction on Test Data for - ", ticker_name)
        st.write(test_data[['Date', 'Close', 'Predicted']])
        st.write("Plotting Close Price vs Predicted Price for - ", models)

        # Plotting the Graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=test_data['Date'], y=test_data['Close'], mode='lines', name='Close'))
        fig.add_trace(go.Scatter(x=test_data['Date'], y=test_data['Predicted'], mode='lines', name='Predicted'))
        fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01), height=550, width=800,
                          autosize=False, margin=dict(l=25, r=75, b=100, t=0))

        st.plotly_chart(fig)

    # Sidebar Menu -----------------------

    menu = ["Train Model"]
    st.sidebar.title("Settings")
    st.sidebar.subheader("Timeseries Settings")
    choices = st.sidebar.selectbox("Select the Activity", menu, index=0)

    if choices == 'Train Model':
        st.subheader("Train Machine Learning Models for Stock Prediction")
        st.markdown('')
        st.markdown('**_Select_ _Stocks_ _to_ Train**')
        stock_select = st.selectbox("", stocks, index=0)
        df1 = load_data(stock_select)
        df1 = df1.reset_index()
        df1['Date'] = pd.to_datetime(df1['Date']).dt.date
        options = ['Select your option', 'Linear Regression', 'LSTM']
        st.markdown('')
        st.markdown('**_Select_ _Machine_ _Learning_ _Algorithms_ to Train**')
        models = st.selectbox("", options)
        submit = st.button('Train Model')

        if models == 'LSTM':
            st.markdown('')
            st.markdown('')
            st.markdown("**Select the _Number_ _of_ _epochs_ and _batch_ _size_ for _training_ form the following**")
            st.markdown('')
            epoch = st.slider("Epochs", 0, 300, step=1)
            b_s = st.slider("Batch Size", 32, 1024, step=1)
            if submit:
                st.write('**Your _final_ _dataframe_ _for_ Training**')
                st.write(df1[['Date', 'Close']])
                create_train_test_LSTM(df1, epoch, b_s, stock_select)


        elif models == 'Linear Regression':
            if submit:
                st.write('**Your _final_ _dataframe_ _for_ Training**')
                st.write(df1[['Date', 'Close']])
                train_data, test_data = create_train_test_data(df1)
                pred_data = Linear_Regression_model(train_data, test_data)
                prediction_plot(pred_data, test_data, models, stock_select)
