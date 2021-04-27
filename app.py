import streamlit as st
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.preprocessing import MinMaxScaler
import pandas_datareader as pdd
from pandas_datareader import data as web
from keras.models import Sequential
from keras.layers import Dense ,LSTM


# App title
st.markdown('''# Stock Price Prediction App''')


# Sidebar
st.sidebar.subheader('Menu')
start_date = st.sidebar.date_input("Start date", datetime.date(2013, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2019, 3, 31))

# Retrieving tickers data
comp_list = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
tickerSymbol = st.sidebar.selectbox('Stock Name', comp_list) # Select ticker symbol
StockData = yf.Ticker(tickerSymbol) # Get ticker data
tickerDf = StockData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker



# Company information
company_logo = '<img src=%s>' % StockData.info['logo_url']
st.markdown(company_logo, unsafe_allow_html=True)

company_name = StockData.info['longName']
st.header('**%s**' % company_name)
company_MarketCap = StockData.info['marketCap']
st.header('**MarketCap :%s**' % company_MarketCap)

company_sector = StockData.info['sector']
st.header('**Sector :%s**' % company_sector)


# string_summary = tickerData.info['longBusinessSummary']
# st.info(string_summary)

# # Company data
st.header('**Company data**')
st.write(tickerDf.tail())


st.header('**Close price of stock**')
st.write('The closing price is the last price at which the stock traded during the regular trading day.')
st.line_chart(tickerDf.Close)

st.header('**Volume of stock**')
st.write('Volume measures the number of shares traded in a stock or contracts traded in futures or options. Volume can be an indicator of market strength, as rising markets on increasing volume are typically viewed as strong and healthy.')
st.line_chart(tickerDf.Volume)



# @st.cache
# def load_data(ticker):
# 	data = yf.download(ticker,start_date,end_date)
# 	data.reset_index(inplace=True)
# 	return data

# data = load_data(tickerSymbol)
# st.write(data)



data = pdd.DataReader(tickerSymbol,data_source='yahoo',start=start_date, end=end_date)

st.write("----")
st.write(data)

datas= data.filter(['Close'])
dataset = datas.values
x = len(dataset)



#take 60% data fro traning...
traning_data_size = math.ceil(len(dataset)*.5)



#nomalaize data
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)




#TRAINING A DATA
train_data = scaled_data[0:traning_data_size, :]
x_train = []
y_train = []
for i in range(60,len(train_data)):
  x_train.append(train_data[i-60:i,0])
  y_train.append(train_data[i,0])
  if i<=61:
  	pass

#convert array in np array

x_train,y_train = np.array(x_train),np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
print(x_train.shape)
# # build model LSTM
model = Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(LSTM(50,return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))


#compile model
model.compile(optimizer='adam',loss='mean_squared_error')

model.fit(x_train, y_train,batch_size=1, epochs=1)


#test our model
test_data = scaled_data[traning_data_size-60: ,:]
x_test = []
y_test = dataset[traning_data_size:, :]
for i in range(60,len(test_data)):
  x_test.append(test_data[i-60:i, 0])


x_test = np.array(x_test)

x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1],1))

pridication = model.predict(x_test)
pridication = scaler.inverse_transform(pridication)


rmse = np.sqrt(np.mean(pridication - y_test) **2)
print(rmse)


train = data[:traning_data_size]
valid = data[traning_data_size:]
valid['pridication'] = pridication
fig2 =plt.figure(figsize=(18,8))
plt.title('Model LM')
plt.xlabel('Date',fontsize=18)
plt.ylabel('close price in USD $',fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close','pridication']])
plt.legend(['Train','Val','pridication'],loc='lower right')
st.pyplot(fig2)

st.markdown(""" ### project developed by Sameer shaikh ,Ziauddin shaikh, Amaan wahgoo""")
