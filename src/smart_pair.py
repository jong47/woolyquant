import os
from pandas_datareader import data as pdr
import pandas as pd
import openai 
import yfinance as yf
import ctypes
import numpy
import stock_pair

ticks = ["DPZ", "AAPL", "GOOG", "AMD", "GME", "SPY", "NFLX", "BA", "WMT", "GS", "XOM", "NKE", "META", "BRK-B", "MSFT"]
avg_price = {}

def read_csv():
    # data = pdr
    for t in ticks:
        data = pdr.get_data_yahoo(t, start="2022-01-01", end="2023-07-17").to_csv('./data/' + t + '.csv')
        avg_price[t] = data['Adj Close'].mean()

    print(avg_price)

def calculate_avg(stock_return: dict, avg_price: dict) -> None:
    path = "./res/data/"
    adj_close = 0
    sample_size = 384
    for file in os.listdir(path):
        full_path = f'{path}/{file}'
        df = pd.read_csv(full_path)

        # For loop runs until EOF for ea. file. --- Big-O: O(n)
        # We convert from Dataframe to series for ea. file
        stock_name = f'{file}'.split('.csv')[0]
        stock_return[stock_name] = []
        for i, stock in df.iterrows():
            # adj_close += stock.iloc[5] # 5 is for Adj Close
            stock_return[stock_name].append(round(stock.iloc[5], 2))

        # rounded_val = abs(round((adj_close / sample_size), 2))
        # avg_price[stock_name] = stock_return[stock_name]
        adj_close = 0

def main():
    # avg_price = {}
    stock_return = {}
    # covariance = []
    # CALL THIS IF YOU THIS IS YOUR FIRST TIME RUNNING THIS PROGRAM
    read_csv()
    # AFTERWARDS COMMENT IT OUT OTHERWISE YOU WILL MAKE UNNECESSARY CALLS
    
    calculate_avg(stock_return=stock_return, avg_price=avg_price)
    # print(avg_price)
    
    # Covariance = Delta(Return ABC - Average ABC) * (Return XYZ - Average XYZ) / (Sample Size) - 1
    for i in range(0, len(avg_price) - 1):
        for j in range(i + 1, len(avg_price)):
            covariance = stock_pair.calculateCovariance(len(stock_return[ticks[0]]), 
                                        numpy.array(stock_return[ticks[i]]), 
                                        numpy.array(stock_return[ticks[j]]),
                                        avg_price[ticks[i]],
                                        avg_price[ticks[j]])
        
            print(ticks[i] + ' & ' + ticks[j] + ': ', covariance)
    # print(stock_pair.pie(5))
    # Cointegration

if __name__ == "__main__":
    yf.pdr_override()
    main()