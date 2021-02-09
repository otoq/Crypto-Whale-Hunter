import time
from binanceClass import BinanceAnaliz as BiAn
from style import satirYaz

markets = ['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'XRPUSDT', 
           'LTCUSDT', 'EOSUSDT', 'ADAUSDT', 'NEOUSDT', 
           'BNBUSDT','XLMUSDT','TRXUSDT','XEMUSDT',
           'XTZUSDT','VETUSDT','MKRUSDT','FTTUSDT',
           'ETCUSDT','ZILUSDT','ZECUSDT','DOGEUSDT',]

holder = {market: BiAn(market) for market in markets}       # dict icinde objelerimiz oluşturduk

def sonuclariYaz():
    print("MARKET\t\tHACİM\t↓↑\tSON500")
    for key in holder:
        satirYaz(holder[key])

    time.sleep(5)
    for key in holder:
        holder[key].refresh()

def main():
    while True:
        sonuclariYaz()

if __name__ == "__main__":
    main()




# # # # # # # # # # # # # # # # # #
# xrp = BiAn('XRPUSDT')
# neo = BiAn('NEOUSDT')
# satirYaz(holder['XRPUSDT'])
# satirYaz(holder['NEOUSDT'])