from binance.client import Client
from datetime import datetime
from pandas import DataFrame as df
import pandas as pd
import keys

client = Client(api_key=keys.ApiKey, api_secret=keys.SecretKey)

class BinanceAnaliz:
    def __init__(self, market_symbol):
        self.market = market_symbol
        self.refresh()
    
    def refresh(self):
        """Refresh the data by fetching the latest trades and 24hr ticker information."""
        self.df = self.binance_recent_trades()
        self.df24 = self.binance_24hr_ticker()
    
    def binance_recent_trades(self):
        """Fetch the last 500 recent trades for the market symbol."""
        try:
            trades = client.get_recent_trades(symbol=self.market)
            trades_df = df(trades)
            return trades_df
        except Exception as e:
            print(f"Error fetching recent trades for {self.market}: {e}")
            return df()

    def recent_trades_time_interval(self):
        """Calculate the time interval in seconds for the last 500 trades."""
        try:
            trades_df = self.df['time']
            sonuc_sn = (trades_df.max() - trades_df.min()) / 1000
            return float(sonuc_sn)
        except Exception as e:
            print(f"Error calculating time interval for {self.market}: {e}")
            return 0.0

    def recent_trades_quoteQty_sum(self):
        """Calculate the sum of quote quantities for the last 500 trades."""
        try:
            trades_df = self.df['quoteQty'].astype(float)
            return trades_df.sum()
        except Exception as e:
            print(f"Error calculating quote quantity sum for {self.market}: {e}")
            return 0.0
    
    def binance_24hr_ticker(self):
        """Fetch the detailed 24-hour ticker information for the market symbol."""
        try:
            ticker = client.get_ticker(symbol=self.market)
            return ticker
        except Exception as e:
            print(f"Error fetching 24hr ticker for {self.market}: {e}")
            return {}

    def binance_24hr_quoteVolume(self):
        """Get the 24-hour quote volume for the market symbol."""
        try:
            volume = self.df24.get('quoteVolume', 0)
            return float(volume)
        except Exception as e:
            print(f"Error fetching 24hr quote volume for {self.market}: {e}")
            return 0.0
    
    def hacim_degisim(self):
        """Calculate the volume change ratio. If greater than 1, there is an increase; if less than 1, a decrease."""
        try:
            recent_volume = self.recent_trades_quoteQty_sum() / self.recent_trades_time_interval()
            daily_volume = self.binance_24hr_quoteVolume() / (24 * 60 * 60)
            return recent_volume / daily_volume
        except Exception as e:
            print(f"Error calculating volume change for {self.market}: {e}")
            return 0.0
    
    def fiyat_artis_azalis(self):
        """Determine the price movement:
        4 = max price at last trade, 3 = above average, 2 = below average, 1 = min price at last trade, 0 = no clear trend."""
        try:
            prices = self.df['price'].astype(float)
            if prices.max() == prices.iloc[-1]:
                return 4
            elif prices.mean() < prices.iloc[-1]:
                return 3
            elif prices.min() == prices.iloc[-1]:
                return 1
            elif prices.mean() >= prices.iloc[-1]:
                return 2
            else:
                return 0
        except Exception as e:
            print(f"Error determining price movement for {self.market}: {e}")
            return 0
