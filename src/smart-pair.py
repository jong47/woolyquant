from pandas_datareader import data as pdr
import openai 
import yfinance as yf
import invoke
import ctypes
yf.pdr_override()

def main():
    ticks = ["DPZ", "AAPL", "GOOG", "AMD", "GME", "SPY", "NFLX", "BA", "WMT", "GS", "XOM", "NKE", "META", "BRK-B", "MSFT"]
    clib = ctypes.DLL("") 
    for t in ticks:
        pdr.get_data_yahoo(t, start="2022-01-01", end="2023-07-17").to_csv('./data/' + t + '.csv')
    
    # Covariance


    # Cointegration

if __name__ == "__main__":
    main()