from colorama import init, Fore, Back, Style
from collections import defaultdict

import pandas as pd
import datetime
import pyupbit
import time

'''
List of coins

#ticker = "KRW-BTC"                     
#ticker = "KRW-MASK"                     
#ticker = "KRW-SOL"                     
#ticker = "KRW-WCT"                     
#ticker = "KRW-VANA"                     
#ticker = "KRW-ONDO"                     
#ticker = "KRW-STMX"                     
#ticker = "KRW-VIRTUAL"                     
#ticker = "KRW-XRP"                     
#ticker = "KRW-PUNDIX"                     
#ticker = "KRW-LAYER"                   
#ticker = "KRW-NXPC"                   
#ticker = "KRW-SNT"                   
#ticker = "KRW-DEEP"                   
#ticker = "KRW-WAL"                   
#ticker = "KRW-TRUMP"                   
#ticker = "KRW-AERGO"
#ticker = "KRW-ARDR"
#ticker = "KRW-DOGE"
#ticker = "KRW-MASK"
#ticker = "KRW-MEW"                   
#ticker = "KRW-USDT"                   
#ticker = "KRW-PEPE"                   
#ticker = "KRW-KAITO"                   
#ticker = "KRW-SUI"                   
#ticker = "KRW-XEM"                   
#ticker = "KRW-PYTH"                   
#ticker = "KRW-EOS"                   
#ticker = "KRW-ANIME"                   
#ticker = "KRW-SOPH"                   
#ticker = "KRW-POKT"                   
#ticker = "KRW-ONDO"                   
#ticker = "KRW-SAFE"                   
'''


def get_rsi(df: pd.DataFrame, period=14):
    """
    Calculate Relative Strength Index (RSI) using pyupbit data.
    
    :param df: Pandas dataframe retrieved from pyupbit API
    :param period: Period for CCI calculation
    :return: RSI value in string format
    """

    # Price change since previous market day
    df['change'] = df['close'].diff()

    # Highest and lowest price values of previous market day 
    df['up'] = df['change'].apply(lambda x: x if x > 0 else 0)
    df['down'] = df['change'].apply(lambda x: -x if x < 0 else 0)

    # average rise and fall of price 
    df['avg_up'] = df['up'].ewm(alpha=1/period).mean()
    df['avg_down'] = df['down'].ewm(alpha=1/period).mean()

    # RSI Calculation
    df['rs'] = df['avg_up'] / df['avg_down']
    df['rsi'] = 100 - (100 / (1 + df['rs']))

    rsi = str(round(df['rsi'].iloc[-2], 2)).ljust(6, "0")

    return rsi

def get_cci(df: pd.DataFrame, period=20):
    """
    Calculate Commodity Channel Index (CCI) using pyupbit data.
    
    :param df: Pandas dataframe retrieved from pyupbit API
    :param period: Period for CCI calculation
    :return: CCI value in string format
    """

    # Typical Price
    df['TP'] = (df['high'] + df['low'] + df['close']) / 3

    # SMA of Typical Price
    df['SMA_TP'] = df['TP'].rolling(window=period).mean()

    # Mean Deviation (correct way for CCI)
    def mean_deviation(series):
        mean = series.mean()
        return ((series - mean).abs()).mean()

    df['MD'] = df['TP'].rolling(window=period).apply(mean_deviation, raw=False)

    # CCI Calculation
    df['CCI'] = (df['TP'] - df['SMA_TP']) / (0.015 * df['MD'])

    return str(round(df.tail(1)["CCI"].values[0], 2)).ljust(7, "0")

def check_indicator_values(ticker: str, interval: str):

    df = pyupbit.get_ohlcv(ticker, interval=interval)   
    
    #price = pyupbit.get_current_price(ticker)

    rsi = get_rsi(df, 14)
    cci = get_cci(df, 20)

    return rsi, cci

def main():
    running = True

    print("\nRunning indicator analysis...\n")
    while running:
        for ticker in tickers:
            for interval, val in intervals.items():
                rsi, cci = check_indicator_values(ticker, interval)

                print(f"{ticker.ljust(8, ' ')} | Time Frame : {val.ljust(3, ' ')} | RSI : {rsi} | CCI : {cci} | {str(datetime.datetime.now())}")

                if float(rsi)<=RSI_CUTOFF:
                    print(Back.GREEN+"                     ")
                    print(Style.RESET_ALL)

                print()

                time.sleep(SHORT_DELAY)

            print('\n--------------------------------------------\n')

        print(f'\n< Resume after {LONG_DELAY} seconds >\n')
        print('\n--------------------------------------------\n')

        time.sleep(LONG_DELAY)
    return

if __name__=="__main__":

    access_key = "" 
    secret_key = "" 

    upbit = pyupbit.Upbit(access_key, secret_key)

    init(convert=True)

    SHORT_DELAY = 5
    LONG_DELAY = 300 

    RSI_CUTOFF = 30
    CCI_CUTOFF = -100

    tickers = [
        "KRW-BTC",
        "KRW-XRP",
        "KRW-ETH",
        "KRW-SOL",
        "KRW-DOGE",
        "KRW-SHIB",
        "KRW-SUI",
        "KRW-LINK",
        "KRW-ADA",
        "KRW-PEPE",
    ]

    intervals = {
        "minute30": "30m", 
        "minute60": "1h", 
        "minute240": "4h", 
        "day": "D",
    } 

    main()