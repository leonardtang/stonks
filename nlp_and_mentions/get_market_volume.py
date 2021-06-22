from datetime import datetime
import pandas as pd
import requests
from yahoo_finance_api2 import share

pd.set_option('mode.chained_assignment', None)


def aggregate_volume():
    """ Using SPY as a proxy of overall market behavior"""

    print('Getting SPY Volume...')
    spy_share = share.Share('SPY')
    ticker_data = spy_share.get_historical(share.PERIOD_TYPE_YEAR, 2,
                                           share.FREQUENCY_TYPE_DAY, 1)
    dates = ticker_data['timestamp']
    dates = [datetime.fromtimestamp(timestamp / 1e3).strftime('%m-%d-%y') for timestamp in dates]
    volumes = ticker_data['volume']

    historical_volume_df = pd.DataFrame([dates, volumes])
    historical_volume_df = historical_volume_df.transpose()
    historical_volume_df.columns = ['Date', 'Total Volume']
    historical_volume_df.to_csv(f'data/volatility/total_market_volume.csv')


def aggregate_mentions():
    print('Getting Total WSB Mentions...')
    sparse_tickers_df = pd.read_csv('data/stock/historical_stock_mentions.csv')
    sparse_tickers_df = sparse_tickers_df.rename(columns={'Unnamed: 0': 'Date'})
    sparse_tickers_df = sparse_tickers_df.set_index('Date')

    condensed_df = sparse_tickers_df.loc[:, (sparse_tickers_df != 0).any(axis=0)]
    total_mentions = condensed_df[condensed_df.columns[0]]
    for column in condensed_df.columns[1:]:
        total_mentions += condensed_df[column]

    condensed_df['Total Mentions'] = total_mentions
    condensed_df = condensed_df.filter(['Total Mentions'])
    condensed_df.to_csv(f'data/volatility/total_wsb_mentions.csv')


def get_volatility():
    print('Getting Historical Volatility...')
    url = 'https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv'
    response = requests.get(url, allow_redirects=True)
    content = response.content
    csv_file = open('data/volatility/historical_vix.csv', 'wb')
    csv_file.write(content)
    csv_file.close()
    temp_df = pd.read_csv('data/volatility/historical_vix.csv', skiprows=1, error_bad_lines=False)
    temp_df = temp_df.tail(365)
    temp_df.columns = ['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE']
    temp_df.to_csv('data/volatility/historical_vix.csv', index=False)


if __name__ == "__main__":
    aggregate_volume()
    aggregate_mentions()
    get_volatility()
