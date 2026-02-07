# 📈 Financial Stock Dashboard

A full-stack financial data application built with Python. This dashboard provides real-time stock tracking, interactive technical analysis charts, and a personal watchlist feature powered by a local SQLite database.

## 📱 Website Link
https://stockdashboard-kedikztbffesz67rmsv48q.streamlit.app/

## 🚀 Features

* **Real-Time Data Fetching:** Integrates with the `yfinance` API to pull live stock prices, company fundamentals, and financial statements.
* **Interactive Visualizations:**
    * **Candlestick Charts:** Technical analysis using Plotly.
    * **Financial Bar Charts:** Quarterly and Annual Revenue/Income analysis using Altair.
* **SQL-Powered Watchlist:** A persistent "Save to Watchlist" feature that stores key metrics (P/E Ratio, ROE, etc.) in a local SQLite database.
* **Fundamental Analysis:** Displays key financial health metrics like Market Cap, EPS, Dividend Yield, and Debt-to-Equity ratios.
* **Caching:** Implemented `@st.cache_data` to optimize API calls and reduce latency.

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend/Database:** Python, SQLite
* **Data Processing:** Pandas, yfinance
* **Visualization:** Plotly, Altair


## 🖼 Images
<img width="1920" height="1020" alt="Screenshot 2026-01-30 222122" src="https://github.com/user-attachments/assets/14d15392-257a-4288-8442-f07e49c86817" />
<img width="1920" height="1020" alt="Screenshot 2026-01-30 222139" src="https://github.com/user-attachments/assets/0a419d29-8e5c-4a68-863e-77ee013606a6" />
<img width="1920" height="1020" alt="Screenshot 2026-01-30 222149" src="https://github.com/user-attachments/assets/e9e3e246-2b02-43e5-8742-10356856c9af" />
<img width="1920" height="1020" alt="Screenshot 2026-01-30 222157" src="https://github.com/user-attachments/assets/b11b5c9c-d473-4dc9-9deb-2f2aab56001c" />
<img width="1920" height="1020" alt="Screenshot 2026-01-30 222237" src="https://github.com/user-attachments/assets/d4de6768-9171-499a-b8e2-1d0f33b4db9b" />


## 💻 How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Samat-ai/Stock_Dashboard.git](https://github.com/Samat-ai/Stock_Dashboard.git)
    cd Stock_Dashboard
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**
    ```bash
    streamlit run stock_dashboard.py
    ```

## 📂 Project Structure

```text
stock-dashboard/
├── stock_dashboard.py   # Main application logic
├── requirements.txt     # Python dependencies
├── watchlist.db         # Local SQLite database (Auto-generated)
└── README.md            # Project documentation
