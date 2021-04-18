import pandas as pd

ticker_df = pd.read_csv("tickers_and_names.csv")
ticker_df = ticker_df[["ticker", "name"]]
ticker_df["name"] = ticker_df["name"].str.replace("&#39;", "'")

df = pd.read_csv("wsb_fresh_topics.csv")
df

# Get relative frequencies/hotness per trading DAY, and then plot it relative to whatever
print(ticker_df[0:15])
