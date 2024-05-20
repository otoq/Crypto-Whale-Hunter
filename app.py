import time
from binanceClass import BinanceAnaliz as BiAn
from style import satirYaz

print("The app is working. Please wait a moment for the initial data to be received. Please ignore any error messages for the initial few data points.")

markets = [
    'BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'XRPUSDT',
    'LTCUSDT', 'EOSUSDT', 'ADAUSDT', 'NEOUSDT',
    'BNBUSDT', 'XLMUSDT', 'TRXUSDT', 'XEMUSDT',
    'XTZUSDT', 'VETUSDT', 'MKRUSDT', 'FTTUSDT',
    'ETCUSDT', 'ZILUSDT', 'ZECUSDT', 'DOGEUSDT'
]

holder = {market: BiAn(market) for market in markets}  # Create objects in the dictionary

def sonuclariYaz():
    print("#############################################")
    print("MARKET\t\tVOLUME\t↓↑\tLAST500")
    for key in holder:
        try:
            satirYaz(holder[key])
        except Exception as e:
            print(f"Error processing market {key}: {e}")

def main():
    # Initial data retrieval
    for key in holder:
        try:
            holder[key].refresh()
        except Exception as e:
            print(f"Error initializing market {key}: {e}")

    while True:
        sonuclariYaz()
        time.sleep(5)  # Wait before refreshing data
        for key in holder:
            try:
                holder[key].refresh()
            except Exception as e:
                print(f"Error refreshing market {key}: {e}")

if __name__ == "__main__":
    main()
