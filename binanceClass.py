# pip install python-binance
from binance.client import Client
from datetime import datetime
from pandas import DataFrame as df 
import pandas as pd

import keys

client = Client(api_key= keys.ApiKey, api_secret=keys.SecretKey)

class BinanceAnaliz:
    def __init__(self, market_symbol):
        self.market = market_symbol
        self.refresh()
    
    def refresh(self):
        self.df = self.binance_recent_trades()
        self.df24 = self.binance_24hr_ticker()
    
    # # # # # # # # # # # # # # # # # # # # #
    # son 500 işlemi getirir
    def binance_recent_trades(self):
        trades = client.get_recent_trades(symbol=self.market)  
        trades_df = df(trades)
        return trades_df

    # son 500 işlemin kaç sn de gerçekleştiğini verir
    def recent_trades_time_interval(self):
        trades_df = self.df['time']
        sonuc_sn = (trades_df.max() - trades_df.min())/1000
        return float(sonuc_sn)

    # son 500 işlemde baz market(USDT) toplam hacmini verir
    def recent_trades_quoteQty_sum(self):
        trades_df = self.df['quoteQty']
        trades_df = trades_df.astype(float)
        return trades_df.sum()
    
    # # # # # # # # # # # # # # # # # # # # #
    # son 24 saatlik detaylı veriyi getirir
    def binance_24hr_ticker(self):    
        tickers = client.get_ticker(symbol=self.market)   
        return tickers
    
    # son 24 saatlik baz market hacimi (USDT)
    def binance_24hr_quoteVolume(self):
        volume = self.df24['quoteVolume']
        return float(volume)
    
    # hacim artış oranı. 1 den buyukse artış vardır. 1 den kucukse azalış var
    def hacim_degisim(self):
        return (self.recent_trades_quoteQty_sum() / self.recent_trades_time_interval()) / (self.binance_24hr_quoteVolume()/(24*60*60))
    
    # fiyatın azalığ arttığının tespiti. 4=max, 3=ortalama ustu, 2=ortalama altı, 1=min, 0= mala bagladı
    def fiyat_artis_azalis(self):
        prices = self.df['price'].astype(float)
        if prices.max() == prices[499]:
            return 4
        elif prices.mean() < prices[499]:
            return 3
        elif prices.min() == prices[499]:
            return 1
        elif prices.mean() >= prices[499]:
            return 2
        else:
            return 0                                        

# x = BinanceAnaliz('XRPUSDT')
# print(x.df)
# print(x.df['price'].astype(float).mean())
# print(x.df['price'].astype(float)[499])
# print(x.recent_trades_time_interval())
# print(x.recent_trades_quoteQty_sum())
# print(x.df24)
# print(x.binance_24hr_quoteVolume())