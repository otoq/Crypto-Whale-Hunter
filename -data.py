# pip install python-binance
from binance.client import Client
from datetime import datetime
from pandas import DataFrame as df 
import pandas as pd

import keys

# mum grafik için veri üretir
def binance_price():
    client = Client(api_key= keys.ApiKey, api_secret=keys.SecretKey)

    candles = client.get_klines(symbol='XRPUSDT', interval=Client.KLINE_INTERVAL_1HOUR)
    # print(candles) 
    # https://python-binance.readthedocs.io/en/latest/binance.html#binance.client.Client.get_klines
    # adresinde ne oldukları yazıyor

    candles_data_frame = df(candles)
    # print (candles_data_frame)
    # üsttekini datafreme içine koduk

    candles_data_frame_date = candles_data_frame[0]             # ilk sütün zaman damgası

    final_date = []

    for time in candles_data_frame_date:
        readable = datetime.fromtimestamp(int(time/1000))       # binance time milisecond cinsinden olduğu için 1000 e böl
        final_date.append(readable)

    candles_data_frame.pop(11)                                  # 11 sutunu çıkardık
    candles_data_frame[0] = final_date                          # tarihi okunabilir yaptık
    candles_data_frame.rename(columns={0:'date'}, inplace=True) # tarih sütünü ismi date oldu
    candles_data_frame.set_index('date', inplace=True)

    candles_data_frame.columns=['open', 'high', 'low', 'close', 'volume', 'close_time', 'asset_volume',
                                'trade_number', 'taker_buy_base', 'taker_buy_quote']
    return candles_data_frame

# son 500 işlemi getirir
def binance_recent_trades(market_symbol):
    client = Client(api_key= keys.ApiKey, api_secret=keys.SecretKey) 
    trades = client.get_recent_trades(symbol=market_symbol)  
    trades_df = df(trades)
    
    return trades_df

# son 500 işlemin kaç sn de gerçekleştiğini verir
def recent_trades_time_interval(trades_df):
    trades_df = trades_df['time']
    # son 500 emirin gerçekleştiği zaman aralığı
    sonuc_sn = (trades_df.max() - trades_df.min())/1000
    return float(sonuc_sn)

# son 500 işlemde baz market(USDT) toplam hacmini verir
def recent_trades_quoteQty_sum(trades_df):
    trades_df = trades_df['quoteQty']
    trades_df = trades_df.astype(float)
    return trades_df.sum()
    

    


# son 24 saatlik detaylı veri
def binance_24hr_ticker(market_symbol):
    client = Client(api_key= keys.ApiKey, api_secret=keys.SecretKey)
    tickers = client.get_ticker(symbol=market_symbol)   
    
    return tickers

# son 24 saatlik hacim
def binance_24hr_quoteVolume(market_symbol):
    volume = binance_24hr_ticker(market_symbol)['quoteVolume']
    return float(volume)


son_islemler_df = binance_recent_trades('XRPUSDT')
print(son_islemler_df)
print(binance_24hr_quoteVolume('XRPUSDT'))
print(recent_trades_time_interval(son_islemler_df))
print(recent_trades_quoteQty_sum(son_islemler_df))