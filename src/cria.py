import os
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from dotenv import load_dotenv

class Cria:
    def __init__(self) -> None:
        pass


load_dotenv('./src/keys.env')
trading_client = TradingClient(os.getenv("ALPACA_PK"), os.getenv("ALPACA_SK"), paper=True)

              
account = trading_client.get_account()
assets = trading_client.get_asset("AAPL")

if assets.tradable:
    market_order_data = MarketOrderRequest(
                        symbol="AAPL",
                        qty=1,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.DAY
                        )
    
    market_order = trading_client.submit_order(order_data=market_order_data)

    print(market_order)


# for property_name, value in account:
#   print(f"\"{property_name}\": {value}")