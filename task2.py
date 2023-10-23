import yfinance as yf
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta



def store_icici_candle_data():
    ticker_symbol = "ICICIBANK.NS"
    start_time = datetime.now().replace(hour=11, minute=15, second=0)

    end_time = start_time.replace(hour=14, minute=15)

    icici_data = yf.download(ticker_symbol, start=start_time, end=end_time, interval="15m")
    client = MongoClient('mongodb://localhost:27017/')
    db = client['StockPrice']
    collection = db['user']

    for index, row in icici_data.iterrows():
        candle_data = {
            "Timestamp": index,
            "Open": row["Open"],
            "High": row["High"],
            "Low": row["Low"],
            "Close": row["Close"],
            "Volume": row["Volume"],
        }
        collection.insert_one(candle_data)
        print(candle_data)

if __name__ == "__main__":
    scheduler = BlockingScheduler()

    scheduler.add_job(store_icici_candle_data, "interval", minutes=15)

    for _ in range(1):
        scheduler.start()
        store_icici_candle_data()
