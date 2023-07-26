import os
import pandas as pd
import openai 
import yfinance as yf
import ctypes
import numpy
import stock_pair
import json
from pandas_datareader import data as pdr
from statsmodels.regression.linear_model import OLS
from statsmodels.tsa.stattools import adfuller
from dotenv import load_dotenv

GPT_MODEL = "gpt-3.5-turbo-0613"

def read_csv(ticks) -> None:
    for t in ticks:
        pdr.get_data_yahoo(t, start="2021-01-01", end="2023-07-24").to_csv('./res/data/' + t + '.csv')

def get_stock_data(return_percent: dict, mean_price: dict, std_dev: list) -> None:
    path = "./res/data/"
    for file in os.listdir(path):
        full_path = f'{path}/{file}'
        df = pd.read_csv(full_path)

        # For loop runs until EOF for ea. file. --- Big-O: O(n)
        # We convert from Dataframe to series for ea. file
        stock_name = f'{file}'.split('.csv')[0]

        # Pulls in the adj close price in percentage form from yahoo
        data = df['Adj Close'].pct_change().dropna() * 100
        std_dev[stock_name] = df['Adj Close'].pct_change().std() * 100

        # We then store the value in list form and round to pretty our data
        return_percent[stock_name] = data.tolist()

        # Then we calculate the mean percentage as part of the covariance
        mean_price[stock_name] = data.mean()

# def chatGPT_conversation(parameters) -> None:
#     with open('./src/stock_prompt.json') as fp:
#         prompt = json.load(fp)

#     print(type(prompt))

#     response = openai.ChatCompletion.create(model=GPT_MODEL, messages=prompt)
#     # print(prompt)


#     # api_usage = response['usage']

def main():
    load_dotenv('./src/keys.env')
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    ticks = ["DPZ", "AAPL", "GOOGL", "GOOG", "BABA", "JNJ", "JPM", "BAC", "TMO", "AVGO", "CVX", "DHR", "V", "COST", "CRM", "DIS", "CSCO", "QCOM", "AMD", "GME", "SPY", "NFLX", "BA", "WMT", "GS", "XOM", "NKE", "META", "BRK-A", "BRK-B", "MSFT", "AMZN", "NVDA", "TSLA"]
    mean_price = {}
    return_percent = {}
    covariance = {}
    std_dev = {}
    divergences = {}

    read_csv(ticks)
    
    get_stock_data(return_percent=return_percent, mean_price=mean_price, std_dev=std_dev)
    
    # Covariance = Delta(Return ABC - Average ABC) * (Return XYZ - Average XYZ) / (Sample Size) - 1
    print("-------- COVARIANCE/CORRELATION/ADF TEST/P-VAL BETWEEN TWO STOCK PAIRS --------")
    for i in range(0, len(mean_price) - 1):
        for j in range(i + 1, len(mean_price)):
            covariance = stock_pair.calculateCovariance(len(return_percent[ticks[0]]), 
                                                        numpy.array(return_percent[ticks[i]]), 
                                                        numpy.array(return_percent[ticks[j]]),
                                                        mean_price[ticks[i]],
                                                        mean_price[ticks[j]])
            
            # Correlation
            corr = covariance / (std_dev[ticks[i]] * std_dev[ticks[j]])
            if corr > 0.79:
                # Cointegration
                model = OLS(numpy.array(return_percent[ticks[i]]), numpy.array(return_percent[ticks[j]]))
                results = model.fit()

                residuals = results.resid
                regression_slope = results.params
                adf_test = adfuller(residuals)
                p_val = adf_test[1]

                parameters = f'{ticks[i]} {ticks[j]}: {covariance} {corr} {adf_test[0]} {p_val} {regression_slope}'.format(ticks[i], ticks[j], covariance, corr, adf_test[0], p_val, regression_slope)
                print(parameters)
                # chatGPT_conversation(parameters=parameters)
                # if p_val > 0.05:
                #     print(ticks[i] + ' & ' + ticks[j] + ': ' + 'null hypothesis is true')

    # print(return_percent["SPY"])
    # print(return_percent["MSFT"])

if __name__ == "__main__":
    yf.pdr_override()
    main()