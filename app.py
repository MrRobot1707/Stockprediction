import streamlit as st
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime

# App title
st.markdown('''# Stock Price Prediction App''')


# Sidebar
st.sidebar.subheader('Menu')
start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2021, 3, 31))

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
st.write(tickerDf)


st.header('**Close price of stock**')
st.write('The closing price is the last price at which the stock traded during the regular trading day.')
st.line_chart(tickerDf.Close)

st.header('**Volume of stock**')
st.write('Volume measures the number of shares traded in a stock or contracts traded in futures or options. Volume can be an indicator of market strength, as rising markets on increasing volume are typically viewed as strong and healthy.')
st.line_chart(tickerDf.Volume)


# # Bollinger bands
st.header('**Bollinger Bands**')
st.write('Bollinger bands help determine whether prices are high or low on a relative basis. They are used in pairs, both upper and lower bands and in conjunction with a moving average.')
qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

# ####
# #st.write('---')
# #st.write(tickerData.info)
