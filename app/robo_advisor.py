# app/robo_advisor.py 

import csv
import json 
import os
import datetime
from pandas import DataFrame

from dotenv import load_dotenv 
import requests

load_dotenv()

# Defining functions 
def to_usd(my_price):
    return"${0:,.2f}".format(my_price)

def compile_url(symbol):
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY") 
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    return request_url 

def get_response(request_url):
    response = requests.get(request_url)
    
    parsed_response = json.loads(response.text)
    return parsed_response

def transform_response(tsd):    
    day_keys = tsd.keys() 
    days = list(day_keys) 
    return days 

def write_to_csv(rows, csv_filepath):
    csv_headers = ["timestamp", "open", "high", "low","close", "volume"]
    with open(csv_file_path,"w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return True 

#User Input Information & Validation (multiple tickers): 
ticker = ""
stock_list = []
First_message = False
while ticker != "DONE":
    ticker = input("Please input the ticker symbol of the stock you would like to evaluate (e.g. \"AMZN\" \"AAPL\" \"GOOG\"): ")
    ticker = ticker.upper()
    if ticker == "DONE":
        print("Getting data from the Internet...")
    elif ticker.isalpha() and len(ticker) <=5:
        stock_list.append(ticker)
    else:
            print(f"Sorry {ticker} doesn't seem like an existing stock ticker. \nPlease ensure that your choice only contains letters and is five or less characters.")
    if not First_message:
        print("If you have more stocks you wish to evaluate, please continue to input their ticker symbols one at a time, otherwise input \"DONE\" ")
        First_message = True 

for symbol in stock_list:
    request_url = compile_URL(symbol)

    try: 
        parsed_response = get_response(request_url)
        tsd = parsed_response["Time Series (Daily)"] 
        days = transform_response(tsd)

        timeStamps = []
        opens = []
        highs = []
        lows = []
        closes = []
        volumes = []

        for date in days:
            timeStamps.append(date)
            opens.append(tsd[date]["1. open"])
            highs.append(float(tsd[date]["2. high"]))
            lows.append(float(tsd[date]["3. low"]))
            closes.append(tsd[date]["4. close"])
            volumes.append(tsd[date]["5. volume"])

        stocks = {
                'timestamp': timeStamps,
                'open': opens,
                'high': highs,
                'low': lows, 
                'close': closes,
                'volume': volumes
                }
        
        df = DataFrame(stocks)
        csv_file_path = os.path.join(os.path.dirname(__file__),"..","data","prices", "symbol", ".csv")
        export_csv = df.to_csv(csv_file_path, header=True)


        print("-------------------------")
        print("Stock: {symbol}")
        print("-------------------------")
        print("Requesting stock market data...")
        print("-------------------------")

        





# accept user input 

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]



dates = list(tsd.keys())

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)
# breakpoint()

#
# INFO OUTPUTS
# 



    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })

#Formatting the request time and csv filepath (following screencast)
time_now = datetime.datetime.now()
formatted_time_now = time_now.strftime("%Y-%m-%d %H:%M:%S")

formatted_csv_filepath = csv_filepath.split("..")[1]

# Printing/Displaying final results

print(f"Requested at: {formatted_time_now}")
print("-------------------------")
print(f"Latest Data from: {last_refreshed}")
print(f"Latest close: {to_usd(float(latest_close))}")
print(f"Recent high: {to_usd(float(recent_high))}")
print(f"Recent low: {to_usd(float(recent_low))}")
print("-------------------------")
print("Recommendation: BUY!")
print("Because: TODO")
print("-------------------------")
print(f"Writing data to CSV: {formatted_csv_filepath}...")
print("-------------------------")
print("Happy Investing!")
print("-------------------------")

