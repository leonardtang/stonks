import time
import pathlib
import datetime as dt
import pandas as pd
from helpers import nested_dict, clean_ticker_list, preprocess_wsb_df, strip_last_line


def main():
    ticker_df = pd.read_csv("data/crypto/crypto_tickers.csv")
    ticker_df = ticker_df[["ticker", "name"]]
    crypto_tickers = list(ticker_df['ticker'])
    crypto_tickers = clean_ticker_list(crypto_tickers)

    df = pd.read_csv('data/wsb_submissions.csv', parse_dates=["created_utc"], engine='python', encoding='utf-8',
                     error_bad_lines=False)

    date_df = preprocess_wsb_df(df)

    dates = date_df.created_utc.unique()

    historical_mentions = nested_dict()

    f = open("crypto_checkpoint.txt", "w")

    OUT_FILE = pathlib.Path('data/crypto/historical_crypto_mentions.csv')
    if OUT_FILE.exists():
        existing_data = True
        existing_df = pd.read_csv(OUT_FILE)
        str_last_recorded_date = existing_df["Unnamed: 0"].iloc[-1]
        # last_recorded_date = dt.datetime.strptime(str_last_recorded_date, '%Y-%m-%d')
        f.write(f"Last Counted Date: {str_last_recorded_date} \n")
        f.write('Appending to existing crypto mentions data...')
        print(f'Last recorded date: {str_last_recorded_date}')
        print('Appending to existing crypto mentions data...')

        n = 0
        for j in existing_df.index:
            if pd.to_datetime(existing_df.loc[j]["Unnamed: 0"]) >= dt.datetime.now() - dt.timedelta(days=365):
                n = j
                break

        existing_df = existing_df[n:]

    else:
        existing_data = False
        f.write(f"Creating new crypto mentions data...' \n")
        print('Creating new crypto mentions data...')

    f.close()

    if existing_data:
        print("Rewriting old file")
        start_time = time.time()
        existing_df.to_csv(OUT_FILE, index=False)
        strip_last_line(str(OUT_FILE))
        print(f"Took {time.time() - start_time} time to rewrite old file")
        datetime_last_recorded_date = pd.to_datetime(str_last_recorded_date)

    for i, date in enumerate(dates):

        date = date.astype('datetime64[us]').astype(dt.datetime)

        if existing_data:
            if date < datetime_last_recorded_date:
                continue

        # Log the most recent cleaned date to resume cleaning from in the event that your machine dies, restarts, etc.
        f = open("crypto_checkpoint.txt", "a")
        str_date = date.strftime("%b %d %Y")

        print(f"Counting Mentions for {str_date}")
        f.write(f"Counting Mentions for {str_date} \n")

        start = time.time()

        filtered_df = date_df[date_df["created_utc"].isin(pd.date_range(date, date))]
        for j, ticker in enumerate(crypto_tickers):
            # Returns a Series of exact-match counts in the length of the number of submissions on the given day
            exact_count = filtered_df.text.str.count(f'(?<!\\S){ticker}(?!\\S)')
            running_count = exact_count.sum()
            name = ticker + 'COIN'
            spellings = [name, name.lower(), name.capitalize()]
            for spelling in spellings:
                soft_count = filtered_df.text.str.count(f'(?<!\\S){spelling}(?!\\S)')
                running_count += soft_count.sum()

            historical_mentions[ticker][date] = running_count

        delta = time.time() - start

        print(f"Compute Time: {delta} \n")
        f.write(f"Compute Time: {delta} \n\n")
        f.close()

        historical_df = pd.DataFrame(historical_mentions)

    if existing_data:
        historical_df.to_csv(OUT_FILE, mode='a', header=False)
    else:
        historical_df.to_csv(OUT_FILE)


if __name__ == "__main__":
    main()
