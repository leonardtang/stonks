import pathlib
import time
import pandas as pd
import datetime as dt
from helpers import clean_ticker_list, preprocess_wsb_df, nested_dict, strip_last_line

PROCESSED_SUBMISSIONS = 'data/processed_wsb_submissions.csv'


def main():
    ticker_df = pd.read_csv(pathlib.Path("data/stock/stock_tickers.csv"))
    ticker_df = ticker_df[["ticker", "name"]]
    ticker_df["name"] = ticker_df["name"].str.replace("&#39;", "'")
    stock_tickers = list(ticker_df["ticker"])
    stock_tickers = clean_ticker_list(stock_tickers)

    print('Reading CSV')
    date_df = pd.read_csv('data/wsb_submissions.csv',
                          parse_dates=["created_utc"],
                          engine='python',
                          encoding='utf-8',
                          error_bad_lines=False)

    date_df = preprocess_wsb_df(date_df)
    date_df.to_csv(PROCESSED_SUBMISSIONS)

    unique_dates = date_df.created_utc.unique()

    historical_mentions = nested_dict()

    f = open("stock_checkpoint.txt", "w")

    OUT_FILE = pathlib.Path('data/stock/historical_stock_mentions.csv')
    if OUT_FILE.exists():
        existing_data = True
        existing_df = pd.read_csv(OUT_FILE, engine='python', encoding='utf-8', error_bad_lines=False)
        str_last_recorded_date = existing_df["Unnamed: 0"].iloc[-1]
        # str_last_recorded_date = pd.to_datetime(last_recorded_date)
        f.write(f"Last Counted Date: {str_last_recorded_date} \n")
        f.write('Appending to existing stock mentions data...')
        print(f'Last recorded date: {str_last_recorded_date}')
        print('Appending to existing stock mentions data...')

        n = 0
        for j in existing_df.index:
            if pd.to_datetime(existing_df.loc[j]["Unnamed: 0"]) >= dt.datetime.now() - dt.timedelta(days=365):
                n = j
                break

        existing_df = existing_df[n:]

    else:
        existing_data = False
        print('Creating new stock mentions data...')

    f.close()

    if existing_data:
        print("Rewriting old file")
        start_time = time.time()
        existing_df.to_csv(OUT_FILE, index=False)
        strip_last_line(str(OUT_FILE))
        print(f"Took {time.time() - start_time} time to rewrite old file")
        datetime_last_recorded_date = pd.to_datetime(str_last_recorded_date)

    for i, date in enumerate(unique_dates):

        date = date.astype('datetime64[us]').astype(dt.datetime)

        if existing_data:
            if date < datetime_last_recorded_date:
                continue

        # Log the most recent cleaned date to resume cleaning from in the event that your machine dies, restarts, etc.
        f = open("stock_checkpoint.txt", "a")
        str_date = date.strftime("%b %d %Y")
        print(f"Counting Mentions for {str_date}")
        f.write(f"Counting Mentions for {str_date} \n")
        start = time.time()

        filtered_df = date_df[date_df["created_utc"].isin(pd.date_range(date, date))]

        # Most recent WSB page
        if i == len(unique_dates) - 1:
            filtered_df.to_csv('data/wsb_daily_text.csv')

        for j, ticker in enumerate(stock_tickers):
            # Returns a Series of exact-match counts in the length of the number of submissions on the given day
            count = filtered_df.text.str.count(f'(?<!\\S){ticker}(?!\\S)')
            historical_mentions[ticker][date] = count.sum()

        delta = time.time() - start
        print(f"Compute Time: {delta}")
        f.write(f"Compute Time: {delta} \n\n")
        f.close()

    historical_df = pd.DataFrame(historical_mentions)

    if existing_data:
        historical_df.to_csv(OUT_FILE, mode='a', header=False)
    else:
        historical_df.to_csv(OUT_FILE)


if __name__ == "__main__":
    main()
