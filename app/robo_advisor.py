# app/robo_advisor.py 

import csv
import json 
import os
import datetime

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


# Information Input 





# accept user input 







last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

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


csv_file_path = os.path.join(os.path.dirname(__file__),"..","data","prices.csv")

csv_headers = ["timestamp", "open", "high", "low","close", "volume"]

with open(csv_file_path,"w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()
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
print("-------------------------")
print("Stock: {symbol}")
print("-------------------------")
print("Requesting stock market data...")
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

