# app/robo_advisor.py 

import csv
import json 
import os
import datetime
from pandas import DataFrame
import statistics
import matplotlib

from dotenv import load_dotenv 
import requests



# Defining functions 
def to_usd(number):
    number = float(number)
    return"${0:,.2f}".format(number)
    return number 

def compile_url(stock_ticker):
    load_dotenv()
    API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY") 
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}".format(stock_ticker, API_KEY)
    return request_url

def get_response(request_url):
    #issues request
    response = requests.get(request_url)
    #parses this data from json to dict

    parsed_response = json.loads(response.text)
    return parsed_response

def transform_response(tsd):
    #Gets list of all keys in tsd (days) and converts to list
    day_keys = tsd.keys() #> 'dict_keys' of all the day values
    days = list(day_keys) #> 'list' of all the day values
    return days

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

        print("-------------------------")
        print("Stock: {symbol}")
        print("-------------------------")
        print("Requesting stock market data...")
        print("-------------------------")


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

        print("Data has been stored successfully")

        #Formatting the request time 
        time_now = datetime.datetime.now()
        formatted_time_now = time_now.strftime("%Y-%m-%d %H:%M:%S")
        print("-------------------------")
        print(f"Requested at: {formatted_time_now}")

        #Getting the latest data 
        last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
        print("-------------------------")
        print(f"Latest Data from: {last_refreshed}")

        #Latest close 
        latest_close = tsd[days[0]]["4. close"]
        print("Latest close: ".ljust(35) + to_USD(latest_close).rjust(10))


        #Recent High 
        recent_high = max(highs)
        print("Recent high: ".ljust(35) + to_USD(recent_high).rjust(10))

        #Recent Low 
        recent_low = min(lows)
        print("Recent low: ".ljust(35) + to_USD(recent_low).rjust(10))

        #Calculating purchase decision 
        difference = recent_high - recent_low
        average_high = statistics.mean(highs)
        average_low = statistics.mean(lows)
        averageStockPrice = (average_high + average_low)/2
        percentDifference = difference / averageStockPrice

        if riskLevelMessage == False:
            risk = .2

            riskLevel = input("How much risk are you willing to take on in this investment?\n enter \"HIGH\", \"MED\", or \"LOW\": ")
            riskLevel = riskLevel.upper()
            
            if riskLevel == "HIGH":
                risk = .3
            elif riskLevel == "MED":
                risk = .2
            elif riskLevel == "LOW":
                risk = .1
            else:
                print("Invalid input, reverting to default risk value of 20% volatility.") 
            
            print("-------------------------")
            riskLevelMessage = True


        # Recommendation based on BFM knowledge 
        print("Evaluating stock purchase decision...")
        print("Recommendation: ")
        if percentDifference > risk and float(latest_close) < recent_low:
            print(" You should buy " + symbol + " because it has an above average volatility for you, with a below average closing price,\n Hence, this stock could have a big jump up.") 
        elif float(lates_close) < recent_low:
            print(" Even if " + symbol + " is at a relative low, you should not buy it as it is not as volatile as you indicated you were willing to risk and, \n Hence, you will not earn as much money.")
        else:
            print(" You should not buy " + symbol + " because it is not very volatile nor is it at a relative low. \n If you do purchase it is recommended that you wait until its price is at or below " + to_USD(average_low) + ".")

        print("-------------------------")

        
        #Matplotlib Graphs
        
        graphDecision = input("Would like to see a graph of this stock value ? Input \"YES\" or press enter: ")
        graphDecision = graphDecision.upper()

        if graphDecision == "YES":
            dayPlot = []
            x = len(highs)

            for number in highs:
                dayPlot.append(x)
                x = x-1

            plt.plot(dayPlot, highs)
            plt.plot(dayPlot, lows)
            plt.title("Graph of " + symbol + " High and Low values over the past 100 days")
            plt.ylabel("Stock Values in USD ($)")
            plt.xlabel("Days")
            plt.show()

        nextStock = 0
        nextStock = nextStock + 1

        if nextStock < len(stock_list) and graphDecision == "YES":
            Continue = input("Please close out of graph and press enter to view stock information on " + stock_list[nextStock] + ": ")
            print("-------------------------")
            print("-------------------------")
        elif nextStock < len(stock_list):
            Continue = input("Press enter to view stock information on " + stock_list[nextStock] + ": ")
            print("-------------------------")
            print("-------------------------")
        else:
            print("\nAll stocks have been viewed.")

    except requests.exceptions.ConnectionError:
        print("Sorry we can't find any trading data for " + symbol + ".")
    except KeyError:
        print("Sorry we can't find any trading data for " + symbol + ".")

