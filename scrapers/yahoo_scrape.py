import pandas as pd
import sys
import os
from datetime import datetime
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nlp_and_mentions import helpers


def get_prices(sparse_tickers_df, mode='stock'):
    print(f'Getting Yahoo Finance Prices for {mode}...')
    sparse_tickers_df = sparse_tickers_df.rename(columns={'Unnamed: 0': 'Date'})
    sparse_tickers_df = sparse_tickers_df.set_index('Date')

    condensed_df = sparse_tickers_df.loc[:, (sparse_tickers_df != 0).any(axis=0)]

    to_drop = [column for column in condensed_df.columns if column in helpers.nltk_stopwords]

    condensed_df = condensed_df.drop(columns=to_drop)
    s = condensed_df.sum()

    top_df = condensed_df[s.sort_values(ascending=False).index[:min(20, len(condensed_df.columns))]]
    if mode == 'crypto':
        top_df = top_df.rename(columns=lambda x: x + '-USD')
    top_df.to_csv(f'data/{mode}/top_{mode}_mentions.csv')
    top_df.head()

    open_data = helpers.nested_dict()
    close_data = helpers.nested_dict()
    high_data = helpers.nested_dict()
    low_data = helpers.nested_dict()
    volume_data = helpers.nested_dict()

    for ticker in top_df.columns:

        print(f"Getting Price Data for: {ticker}")
        this_share = share.Share(ticker)

        try:
            ticker_data = this_share.get_historical(share.PERIOD_TYPE_YEAR, 1,
                                                    share.FREQUENCY_TYPE_DAY, 1)
        except YahooFinanceError as e:
            print(e.message)
            continue

        for i, timestamp in enumerate(ticker_data['timestamp']):
            date = datetime.fromtimestamp(timestamp / 1e3).strftime('%m-%d-%y')
            open_data[date][ticker] = ticker_data['open'][i]
            close_data[date][ticker] = ticker_data['close'][i]
            high_data[date][ticker] = ticker_data['high'][i]
            low_data[date][ticker] = ticker_data['low'][i]
            volume_data[date][ticker] = ticker_data['volume'][i]

    open_df = pd.DataFrame.from_dict(open_data, orient='index')
    open_df.tail()

    close_df = pd.DataFrame.from_dict(close_data, orient='index')
    high_df = pd.DataFrame.from_dict(high_data, orient='index')
    low_df = pd.DataFrame.from_dict(low_data, orient='index')
    volume_df = pd.DataFrame.from_dict(volume_data, orient='index')

    open_df.to_csv(f'data/{mode}/open_{mode}_data.csv')
    close_df.to_csv(f'data/{mode}/close_{mode}_data.csv')
    high_df.to_csv(f'data/{mode}/high_{mode}_data.csv')
    low_df.to_csv(f'data/{mode}/low_{mode}_data.csv')
    volume_df.to_csv(f'data/{mode}/volume_{mode}_data.csv')


def main():
    stock_df = pd.read_csv('data/stock/historical_stock_mentions.csv')
    crypto_df = pd.read_csv('data/crypto/historical_crypto_mentions.csv')
    get_prices(stock_df, mode='stock')
    get_prices(crypto_df, mode='crypto')


if __name__ == "__main__":
    main()
