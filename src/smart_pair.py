# Native Python Modules
import os
import json
import ast
from multiprocessing import Pool

# Dependencies
import pandas as pd
import openai 
import yfinance as yf
import numpy
from pandas_datareader import data as pdr
from statsmodels.regression.linear_model import OLS
from statsmodels.tsa.stattools import adfuller
from dotenv import load_dotenv

# Local Files
import stock_pair


class ChatGPT:
    def __init__(self) -> None:
        self.GPT_MODEL = "gpt-3.5-turbo"
        self.__load_api_key()

    def __load_api_key(self) -> None:
        load_dotenv('./src/keys.env')
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def chatGPT_conversation(self, pair, parameters) -> None:
        with open('./src/pairs_trading_prompt.json') as fp:
            prompt = json.load(fp)
        
        # prompt['content'] = parameters
        messages = [{ "role": "user", "content": f'{prompt} {parameters}' }]

        response = openai.ChatCompletion.create(model=self.GPT_MODEL, messages=messages)

        content = response.choices[0].message["content"].replace('\"', '\\"').replace('\\n', '\\""').replace('\\\\"', '\\"')
        data = json.loads(content)
            
        with open(f'./res/data/pairs/{pair}.json', 'w', encoding='utf-8') as f:
            ast.literal_eval(json.dump(data, f, ensure_ascii=False, indent=4))

        print(response)

        api_usage = response['usage']
        print("\n\nCURRENT API USAGE\n\n", api_usage)

class SmartPair:
    def __init__(self) -> None:
        self.equity_info = {}
        self.percent_return = {}
        self.price_return = {}
        self.mean_percent_return = {}
        self.mean_price_return = {}
        self.covariance = {}
        self.std_dev = {}
        self.spread_series = {}

        self.chat_gpt = ChatGPT()

    def read_csv(self, ticks) -> None:
        for t in ticks:
            pdr.get_data_yahoo(t, start="max").to_csv('./res/data/stocks/' + t + '.csv')
    
    def get_stock_data(self) -> None:
        path = "./res/data/stocks"
        for file in os.listdir(path):
            full_path = f'{path}/{file}'
            df = pd.read_csv(full_path)

            # For loop runs until EOF for ea. file. --- Big-O: O(n)
            # We convert from Dataframe to series for ea. file
            ticker = f'{file}'.split('.csv')[0]

            self.equity_info[ticker] = df

            # Pulls in the adj close price in percentage form
            percent_data = df['Adj Close'].pct_change().dropna() * 100

            # Pulls in the adj close price in normal value form
            value_data = df['Adj Close'].dropna()
            
            # Calculates standard deviation of Adj Close values, removes any NaN values, and rounds to 4 decimal places
            self.std_dev[ticker] = percent_data.std()

            # We then store the value in list form and round to pretty our data
            self.percent_return[ticker] = percent_data.to_numpy()
            self.price_return[ticker] = value_data.to_numpy()

            # Then we calculate the mean percentage as part of the covariance
            self.mean_percent_return[ticker] = percent_data.mean()
            self.mean_price_return[ticker] = value_data.mean()
    
    # NOTE: This function assumes that the stock pairs being passed in args are highly correlated.
    # Returns an aligned time series list of stock pairs, where [0] is the left_equity and [1] is the right_equity 
    def align_time_series(self, left_equity, right_equity) -> list:
            curr_start = left_equity.first_valid_index()
            curr_end = left_equity.last_valid_index()

            next_start = right_equity.first_valid_index()
            next_end = right_equity.last_valid_index()

            start = max(curr_start, next_start)
            end = min(curr_end, next_end)

            return list(left_equity.loc[start:end], right_equity.loc[start:end])
    


def main():
    ticks = ["DPZ", "AAPL", "GOOGL", "GOOG", "BABA", "JNJ", "JPM", "BAC", "TMO", 
             "AVGO", "CVX", "DHR", "V", "MA", "COST", "CRM", "DIS", "CSCO", "QCOM", "AMD", 
             "GME", "SPY", "NFLX", "BA", "WMT", "GS", "XOM", "NKE", "META", "BRK-A", 
             "BRK-B", "MSFT", "AMZN", "NVDA", "TSLA"]
    sp = SmartPair()
    sp.load_api_key()


    sp.read_csv(ticks)

    sp.get_stock_data()
    
    # Covariance = Delta(Return ABC - Average ABC) * (Return XYZ - Average XYZ) / (Sample Size) - 1
    # print("-------- COVARIANCE/CORRELATION/ADF TEST/P-VAL BETWEEN TWO STOCK PAIRS --------")

    sp.analyze_time_series(ticks)

    while ticks:
        left = ticks.pop()
        right = ticks[0]


    for i in range(0, len(mean_percent_return) - 1):
        for j in range(i + 1, len(mean_percent_return)):
            covariance = stock_pair.calculateCovariance(sample_size, 
                                                        percent_return[ticks[i]], 
                                                        percent_return[ticks[j]],
                                                        mean_percent_return[ticks[i]],
                                                        mean_percent_return[ticks[j]])
            
            # Correlation
            corr = covariance / (std_dev[ticks[i]] * std_dev[ticks[j]])

            # Check if the correlation is really high before we decide pairs
            if corr > 0.79:
                # Cointegration
                model = OLS(percent_return[ticks[i]], percent_return[ticks[j]])
                results = model.fit()

                residuals = results.resid
                regression_slope = results.params
                adf_test = adfuller(residuals)
                p_val = adf_test[1]

                pair = f'{ticks[i]}-{ticks[j]}'
                
                spread_series[pair] = stock_pair.calculateAverageSpread(sample_size, price_return[ticks[i]], price_return[ticks[j]])

                # parameters = f'{pair}: {covariance} {corr} {adf_test[0]} {p_val} {regression_slope} {spread_series[pair]} {mean_price_return[ticks[i]]} {mean_price_return[ticks[j]]}'
                # print(parameters)
                # chatGPT_conversation(pair=pair, parameters=parameters)
                
                # Price
                numpy.savetxt(f'./res/data/stocks/{ticks[i]}-price-series.csv', price_return[ticks[i]], delimiter=",")
                numpy.savetxt(f'./res/data/stocks/{ticks[j]}-price-series.csv', price_return[ticks[j]], delimiter=",")
                
                # Percent
                numpy.savetxt(f'./res/data/stocks/{ticks[i]}-percent-series.csv', percent_return[ticks[i]], delimiter=",")
                numpy.savetxt(f'./res/data/stocks/{ticks[j]}-percent-series.csv', percent_return[ticks[j]], delimiter=",")
            

                

if __name__ == "__main__":
    yf.pdr_override()
    main()