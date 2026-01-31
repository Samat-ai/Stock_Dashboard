import altair as alt # declarative building blocks for interactive visuals
import plotly.graph_objects as go # visuals and graphs
import streamlit as st # useful framework for developing data apps
import yfinance as yf # fetch financial data from Yahoo
import sqlite3 # saving user watchlist
import pandas as pd # display user watchlist data


# initialize the database (creates the file if it doesn't exist)
def init_db():
    conn = sqlite3.connect('watchlist.db')
    c = conn.cursor()
    # create table if it doesn't exist already
    c.execute('''
              CREATE TABLE IF NOT EXISTS watchlist (
                 symbol TEXT PRIMARY KEY,
                 pe_ratio REAL,
                 pb_ratio REAL,
                 roe REAL)''')
    conn.commit()
    conn.close()

# add a stock to the database
def add_to_watchlist(symbol, info):
    conn = sqlite3.connect('watchlist.db')
    c = conn.cursor()
    try:
        pe = info.get('trailingPE', 0)
        pb = info.get('priceToBook', 0)
        roe = info.get('returnOnEquity', 0)

        c.execute('INSERT INTO watchlist (symbol, pe_ratio, pb_ratio, roe) VALUES (?, ?, ?, ?)', (symbol, pe, pb, roe))
        conn.commit()
        st.success("Saved")
    except sqlite3.IntegrityError:
        st.warning("Exists")
    conn.close()

# read all stocks from the database
def get_watchlist():
    conn = sqlite3.connect('watchlist.db')
    c = conn.cursor()
    c.execute('SELECT symbol FROM watchlist')
    data = c.fetchall()
    conn.close()
    return [row[0] for row in data] # return a clean list of strings

# delete a stock from the database
def remove_from_watchlist(symbol):
    conn = sqlite3.connect('watchlist.db')
    c = conn.cursor()
    c.execute('DELETE FROM watchlist WHERE symbol=?', (symbol,))
    conn.commit()
    conn.close()
    st.rerun() # refresh the app to show the updated list


init_db() #initiate database

# method to fetch stock info from yfinance
@st.cache_data #cache data to prevent redundant API calls
def fetch_stock_info(symbol):
    stock = yf.Ticker(symbol) # ticker obj
    return stock.info

# method for quarterly reports
@st.cache_data #cache data to prevent redundant API calls
def fetch_quarterly_financials(symbol):
    stock = yf.Ticker(symbol) # ticker obj
    return stock.quarterly_financials.T

# method for annual reports
@st.cache_data #cache data to prevent redundant API calls
def fetch_annual_financials(symbol):
    stock = yf.Ticker(symbol) # ticker obj
    return stock.financials.T

# method for candlestick patterns
@st.cache_data # cache data to prevent redundant API calls
def fetch_weekly_price_history(symbol):
    stock = yf.Ticker(symbol) # ticker obj
    return stock.history(period='1y', interval='1wk') # period shows price history for 1 year, interval shows price of stock w/ 1 week between them

# title of website
st.title('Stock Dashboard')

# header for watchlist on sidebar
st.sidebar.header('My Watchlist')
watchlist = get_watchlist()

for saved_symbol in watchlist:
    col1, col2 = st.sidebar.columns([4, 1]) # delete from watchlist button position
    with col1:
        st.write(saved_symbol)
    with col2:
        if st.button("X", key=f'del_{saved_symbol}'):
            remove_from_watchlist(saved_symbol)

# show watchlist button creation
if st.sidebar.button("Show Watchlist Data"):
    conn = sqlite3.connect('watchlist.db')
    # showing SQL table with pandas
    df = pd.read_sql_query("SELECT * FROM watchlist", conn)
    conn.close()

    st.write("### :blue[Watchlist Fundamentals]")
    st.dataframe(df)  # shows an interactive table of your saved stocks

# place where user inputs stock name
symbol = st.sidebar.text_input('Enter a stock symbol')

if symbol: # only run if 'symbol' is not empty
    try:
        # this code only runs after the user types something and hits Enter
        information = fetch_stock_info(symbol)

        st.header(':blue[Company Information]')
        col1, col2 = st.columns(2)  # 3 columns for layout
        with col1:
            st.metric("Company Name", information.get("longName", symbol))
        with col2:
            st.metric("Sector", information.get("sector", "N/A"))

        st.subheader(f'Market Cap: ${information["marketCap"]:,}')


        st.header(':blue[Fundamental Analysis]')
        # give user PE, P/B, ROE, EPS, Dividend Yield
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            pe_ratio = information.get('trailingPE', 'N/A')
            st.metric('PE Ratio', f'{pe_ratio:.2f}' if isinstance(pe_ratio, float) else pe_ratio)
        with col2:
            pb_ratio = information.get('priceToBook', 'N/A')
            st.metric("P/B Ratio", f'{pb_ratio:.2f}' if isinstance(pb_ratio, float) else pb_ratio)
        with col3:
            roe = information.get('returnOnEquity', 'N/A')
            st.metric('ROE', f'{roe*100:.2f}' if isinstance(roe, float) else roe)

        col5, col6, col7, col8 = st.columns(4)
        with col5:
            eps = information.get('trailingEps', 'N/A')
            st.metric('EPS', f'{eps:.2f}' if isinstance(eps, float) else eps)
        with col6:
            div_yield = information.get('dividendYield', 'N/A')
            val = f"{div_yield*100:.2f}%" if isinstance(div_yield, float) else "None"
            st.metric("Dividend Yield", val)

        # creates wishlist button on sidebar
        col1, col2 = st.sidebar.columns([4, 1])
        with col1:
            st.header(f'{information.get("longName", symbol)}')
        with col2:
            if st.button("❤"):
                add_to_watchlist(symbol, information)

        # chart creation
        price_history = fetch_weekly_price_history(symbol)
        st.header(':blue[Chart]')

        price_history = price_history.rename_axis('Date').reset_index()
        candle_stick_chart = go.Figure(data=[go.Candlestick(x=price_history['Date'],
                                       open=price_history['Open'],
                                       low=price_history['Low'],
                                       high=price_history['High'],
                                       close=price_history['Close'])])

        candle_stick_chart.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(candle_stick_chart, use_container_width=True)

        quarterly_financials = fetch_quarterly_financials(symbol)
        annual_financials = fetch_annual_financials(symbol)


        st.header(':blue[Financials]')
        selection = st.segmented_control(label='Period', options=['Quarterly', 'Annual'], default='Quarterly')

        if selection == 'Quarterly':
            quarterly_financials = quarterly_financials.rename_axis('Quarter').reset_index()
            quarterly_financials['Quarter'] = quarterly_financials['Quarter'].astype(str)
            fmt = "," #formatting to separate thousands

            # base chart
            base = alt.Chart(quarterly_financials).encode(x='Quarter:O')

            # layering bars: Revenue(Green) / Income(Blue)
            revenue_chart = base.mark_bar(color='#2ecc71', opacity=0.7).encode(
                y=alt.Y('Total Revenue', axis=alt.Axis(title='Total Revenue')),
                tooltip=["Quarter", alt.Tooltip('Total Revenue', format=fmt)]
            )

            income_chart = base.mark_bar(color='#3498db').encode(
                y=alt.Y('Net Income', axis=alt.Axis(title='Net Income')),
                tooltip=["Quarter", alt.Tooltip('Net Income', format=fmt)]
            )

            # combining both charts
            st.altair_chart(revenue_chart + income_chart, use_container_width=True)

        if selection == 'Annual':
            annual_financials = annual_financials.rename_axis('Year').reset_index()
            annual_financials['Year'] = annual_financials['Year'].astype(str).transform(lambda year: year.split('-')[0])
            fmt = ","

            base = alt.Chart(annual_financials).encode(x='Year:O')

            revenue_chart = base.mark_bar(color='#2ecc71', opacity=0.7).encode(
                y=alt.Y('Total Revenue', axis=alt.Axis(title='Total Revenue')),
                tooltip=["Year", alt.Tooltip('Total Revenue', format=fmt)]
            )

            income_chart = base.mark_bar(color='#3498db').encode(
                y=alt.Y('Net Income', axis=alt.Axis(title='Net Income')),
                tooltip=["Year", alt.Tooltip('Net Income', format=fmt)]
            )

            st.altair_chart(revenue_chart + income_chart, use_container_width=True)

    # intercept errors, so the website doesn't crash
    except Exception as error:
        # this catches cases where they type a fake ticker
        st.error(f"Could not find stock data for '{symbol}'. Please check the ticker.")
else:
    # message when symbol box is empty
    st.info("Waiting for input... Please enter a stock ticker (e.g. MSFT) to begin.")