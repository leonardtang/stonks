import pandas as pd
import numpy as np
import redditcleaner
from collections import defaultdict
from pprint import pprint

ticker_df = pd.read_csv("tickers_and_names.csv")
ticker_df = ticker_df[["ticker", "name"]]
ticker_df["name"] = ticker_df["name"].str.replace("&#39;", "'")

df = pd.read_csv('wsb_truncated.csv', parse_dates=["created_utc"], engine='python', encoding='utf-8', error_bad_lines=False)

df = df.replace(np.nan, '', regex=True)
df = df.replace({'\[removed\]': ''}, regex=True)

df['selftext'] = df['selftext'].map(redditcleaner.clean)
df['title'] = df['title'].map(redditcleaner.clean)

stock_tickers = list(ticker_df["ticker"])
stop_tickers = ["YOLO", "PUMP", "RH", "EOD", "IPO", "ATH", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
blacklist_words = [
      "YOLO", "TOS", "CEO", "CFO", "CTO", "DD", "BTFD", "WSB", "OK", "RH",
      "KYS", "FD", "TYS", "US", "USA", "IT", "ATH", "RIP", "BMW", "GDP",
      "OTM", "ATM", "ITM", "IMO", "LOL", "DOJ", "BE", "PR", "PC", "ICE",
      "TYS", "ISIS", "PRAY", "PT", "FBI", "SEC", "GOD", "NOT", "POS", "COD",
      "AYYMD", "FOMO", "TL;DR", "EDIT", "STILL", "LGMA", "WTF", "RAW", "PM",
      "LMAO", "LMFAO", "ROFL", "EZ", "RED", "BEZOS", "TICK", "IS", "DOW"
      "AM", "PM", "LPT", "GOAT", "FL", "CA", "IL", "PDFUA", "MACD", "HQ",
      "OP", "DJIA", "PS", "AH", "TL", "DR", "JAN", "FEB", "JUL", "AUG",
      "SEP", "SEPT", "OCT", "NOV", "DEC", "FDA", "IV", "ER", "IPO", "RISE"
      "IPA", "URL", "MILF", "BUT", "SSN", "FIFA", "USD", "CPU", "AT",
      "GG", "ELON", "EV"
]
stop_tickers = set(stop_tickers).union(set(blacklist_words))
stock_tickers = [ticker for ticker in stock_tickers if ticker not in stop_tickers]

df['text'] = df.selftext.astype(str).str.cat(df.title.astype(str), sep='. ')
df = df.drop(columns=["selftext", "title"])

date_df = df.copy()
date_df["created_utc"] = pd.to_datetime(df['created_utc'], utc=True)
date_df["created_utc"] = date_df["created_utc"].dt.date.astype("datetime64")


def inner_dict():
    return {}


def nested_dict():
    return lambda: defaultdict(inner_dict)


dates = date_df.created_utc.unique()

historical_mentions = nested_dict()

for i, date in enumerate(dates[0:2]):
    filtered_df = date_df[date_df["created_utc"].isin(pd.date_range(date, date))][:10]
    for j, ticker in enumerate(stock_tickers):
        # Returns a Series of eaxct-match counts in the length of the number of submissions on the given day
        count = filtered_df.text.str.count(f'(?<!\\S){ticker}(?!\\S)')
        historical_mentions[ticker][date] = sum(count)


historical_df = pd.DataFrame(historical_mentions)

historical_df.to_csv('historical_stock_mentions.csv')