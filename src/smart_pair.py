import os
from pandas_datareader import data as pdr
import pandas as pd
import openai 
import yfinance as yf
import ctypes
import numpy
import stock_pair

def read_csv(ticks):
    for t in ticks:
        pdr.get_data_yahoo(t, start="2021-01-01", end="2023-07-17").to_csv('./res/data/' + t + '.csv')

def calculate_avg(stock_return: dict, avg_price: dict, std_dev: list) -> None:
    path = "./res/data/"
    # adj_close = 0
    sample_size = 384
    for file in os.listdir(path):
        full_path = f'{path}/{file}'
        df = pd.read_csv(full_path)

        # For loop runs until EOF for ea. file. --- Big-O: O(n)
        # We convert from Dataframe to series for ea. file
        stock_name = f'{file}'.split('.csv')[0]
        
        # Pulls in the adj close price in percentage form from yahoo
        data = df['Adj Close'].pct_change() * 100
        std_dev.append(df['Adj Close'].pct_change().std() * 100)

        # We then store the value in list form and round to pretty our data
        stock_return[stock_name] = data.tolist()

        # Then we calculate the mean percentage as part of the covariance
        avg_price[stock_name] = data.mean()

def main():
    avg_price = {}
    stock_return = {}
    covariance = {}
    std_dev = []
    ticks = ["DPZ", "AAPL", "GOOG", "AMD", "GME", "SPY", "NFLX", "BA", "WMT", "GS", "XOM", "NKE", "META", "BRK-B", "MSFT"]

    # CALL THIS IF YOU THIS IS YOUR FIRST TIME RUNNING THIS PROGRAM
    read_csv(ticks)
    # AFTERWARDS COMMENT IT OUT OTHERWISE YOU WILL MAKE UNNECESSARY CALLS
    
    calculate_avg(stock_return=stock_return, avg_price=avg_price, std_dev=std_dev)
    
    # Covariance = Delta(Return ABC - Average ABC) * (Return XYZ - Average XYZ) / (Sample Size) - 1
    print("-------- COVARIANCE/CORRELATION/ BETWEEN TWO STOCK PAIRS --------")
    for i in range(0, len(avg_price) - 1):
        for j in range(i + 1, len(avg_price)):
            # stock_pair_name = '{0} & {1}'.format(ticks[i], ticks[j])
            covariance = stock_pair.calculateCovariance(len(stock_return[ticks[0]]), 
                                                                         numpy.array(stock_return[ticks[i]]), 
                                                                         numpy.array(stock_return[ticks[j]]),
                                                                         avg_price[ticks[i]],
                                                                         avg_price[ticks[j]])
            
            corr = covariance / (std_dev[i] * std_dev[j])

            print(ticks[i] + ' & ' + ticks[j] + ': ', covariance, corr)
            # print(corr)          
            # print(covariance)
            # print(std_a)
            # print(std_b)

            # '{ticks[i]} & {ticks[j]}'.format(ticks[i], ticks[j])

    # Correlation

    # Cointegration

if __name__ == "__main__":
    yf.pdr_override()
    main()