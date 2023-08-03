import os
import pandas as pd
import openai 
import yfinance as yf
# import numpy
import stock_pair
import json
from pandas_datareader import data as pdr
from statsmodels.regression.linear_model import OLS
from statsmodels.tsa.stattools import adfuller
from dotenv import load_dotenv
import ast

GPT_MODEL = "gpt-3.5-turbo"

class SmartPair:
    def __init__(self) -> None:
        self.return_percent = {}
        self.return_price = {}
        self.mean_return_percent = {}
        self.mean_return_price = {}
        self.covariance = {}
        self.std_dev = {}
        self.spread_series = {}


    pass

def read_csv(ticks) -> None:
    for t in ticks:
        pdr.get_data_yahoo(t, start="2021-01-01", end="2023-07-24").to_csv('./res/data/stocks/' + t + '.csv')

def get_stock_data(return_percent: dict, return_price: dict, mean_return_percent: dict, mean_return_price: dict, std_dev: list) -> None:
    path = "./res/data/stocks"
    for file in os.listdir(path):
        full_path = f'{path}/{file}'
        df = pd.read_csv(full_path)

        # For loop runs until EOF for ea. file. --- Big-O: O(n)
        # We convert from Dataframe to series for ea. file
        stock_name = f'{file}'.split('.csv')[0]

        # Pulls in the adj close price in percentage form
        percent_data = df['Adj Close'].pct_change().dropna() * 100

        # Pulls in the adj close price in normal value form
        value_data = df['Adj Close'].dropna()
        
        # Calculates standard deviation of Adj Close values, removes any NaN values, and rounds to 4 decimal places
        std_dev[stock_name] = percent_data.std()

        # We then store the value in list form and round to pretty our data
        return_percent[stock_name] = percent_data.to_numpy()
        return_price[stock_name] = value_data.to_numpy()

        # Then we calculate the mean percentage as part of the covariance
        mean_return_percent[stock_name] = percent_data.mean()
        mean_return_price[stock_name] = value_data.mean()

def chatGPT_conversation(pair, parameters) -> None:
    with open('./src/pairs_trading_prompt.json') as fp:
        prompt = json.load(fp)
    
    # prompt['content'] = parameters
    messages = [{ "role": "user", "content": f'{prompt} {parameters}' }]

    response = openai.ChatCompletion.create(model=GPT_MODEL, messages=messages)

    content = response.choices[0].message["content"].replace('\"', '\\"').replace('\\n', '\\""').replace('\\\\"', '\\"')
    data = json.loads(content)
        
    with open(f'./res/data/pairs/{pair}.json', 'w', encoding='utf-8') as f:
        ast.literal_eval(json.dump(data, f, ensure_ascii=False, indent=4))

    print(response)

    api_usage = response['usage']
    print("\n\nCURRENT API USAGE\n\n", api_usage)

def load_api_key() -> None:
    load_dotenv('./src/keys.env')
    openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    load_api_key()
    ticks = ["DPZ", "AAPL", "GOOGL", "GOOG", "BABA", "JNJ", "JPM", "BAC", "TMO", 
             "AVGO", "CVX", "DHR", "V", "MA", "COST", "CRM", "DIS", "CSCO", "QCOM", "AMD", 
             "GME", "SPY", "NFLX", "BA", "WMT", "GS", "XOM", "NKE", "META", "BRK-A", 
             "BRK-B", "MSFT", "AMZN", "NVDA", "TSLA"]
    return_percent = {}
    return_price = {}
    mean_return_percent = {}
    mean_return_price = {}
    covariance = {}
    std_dev = {}
    spread_series = {}

    read_csv(ticks)

    get_stock_data(return_percent=return_percent, 
                   return_price=return_price, 
                   mean_return_percent=mean_return_percent, 
                   mean_return_price=mean_return_price, 
                   std_dev=std_dev)
    
    # Covariance = Delta(Return ABC - Average ABC) * (Return XYZ - Average XYZ) / (Sample Size) - 1
    # print("-------- COVARIANCE/CORRELATION/ADF TEST/P-VAL BETWEEN TWO STOCK PAIRS --------")
    sample_size = len(return_percent[ticks[0]])
    for i in range(0, len(mean_return_percent) - 1):
        for j in range(i + 1, len(mean_return_percent)):
            covariance = stock_pair.calculateCovariance(sample_size, 
                                                        return_percent[ticks[i]], 
                                                        return_percent[ticks[j]],
                                                        mean_return_percent[ticks[i]],
                                                        mean_return_percent[ticks[j]])
            
            # Correlation
            corr = covariance / (std_dev[ticks[i]] * std_dev[ticks[j]])

            # Check if the correlation is really high before we decide pairs
            if corr > 0.79:
                # Cointegration
                model = OLS(return_percent[ticks[i]], return_percent[ticks[j]])
                results = model.fit()

                residuals = results.resid
                regression_slope = results.params
                adf_test = adfuller(residuals)
                p_val = adf_test[1]

                pair = f'{ticks[i]}-{ticks[j]}'
                
                spread_series[pair] = stock_pair.calculateAverageSpread(sample_size, return_price[ticks[i]], return_price[ticks[j]])

                parameters = f'{pair}: {covariance} {corr} {adf_test[0]} {p_val} {regression_slope} {spread_series[pair]} {mean_return_price[ticks[i]]} {mean_return_price[ticks[j]]}'
                print(parameters)
                chatGPT_conversation(pair=pair, parameters=parameters)

if __name__ == "__main__":
    yf.pdr_override()
    main()