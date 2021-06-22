import pathlib
import pytz
import warnings
import requests
import time
import pandas as pd
import datetime as dt
from urllib3.exceptions import ProtocolError

url = "https://api.pushshift.io/reddit/search/submission"


def crawl_page(subreddit: str, last_page=None, after=int(dt.datetime(2020, 4, 1).timestamp())):
    if last_page is None:
        params = {"subreddit": subreddit,
                  "size": 500,
                  "sort": "asc",
                  "sort_type": "created_utc",
                  "after": after,
                  "stream": True}

    else:
        params = {"subreddit": subreddit,
                  "size": 500,
                  "sort": "asc",
                  "sort_type": "created_utc",
                  "stream": True}

    # Keep crawling subreddit until no more pages
    if last_page is not None:
        if len(last_page) > 0:
            params["after"] = last_page[-1]["created_utc"]
        else:
            return []

    try:
        with requests.get(url, params) as results:
            while not results.ok:
                warnings.warn("Server returned status code {}".format(results.status_code))
                time.sleep(10)
                results = requests.get(url, params)
                if results.ok:
                    print("Server Error Resolved")

            return results.json()["data"]

    except (ProtocolError, requests.exceptions.ChunkedEncodingError):
        pass


def get_date(created):
    est = pytz.timezone('US/Eastern')
    return dt.datetime.fromtimestamp(created, tz=est)


def crawl_subreddit(subreddit):
    submissions = []
    existing_df = None
    last_page = None
    i = 0

    f = open("reddit_scrape_checkpoint.txt", "w")

    out_file = pathlib.Path('data/wsb_submissions.csv')

    if out_file.exists():
        existing_data = True
        existing_df = pd.read_csv(out_file, engine='python', encoding='utf-8', error_bad_lines=False)
        last_recorded_date = existing_df["created_utc"].iloc[-1]
        str_date = pd.to_datetime(last_recorded_date)
        f.write(f"Last Counted Date: {str_date} \n")
        f.write('Appending to existing Reddit data...')
        print(f'Last recorded date: {last_recorded_date}')
        print('Appending to existing Reddit data...')
        print(existing_df.head())

        n = 0
        for j in existing_df.index:
            if pd.to_datetime(existing_df.loc[j]["created_utc"]) >= pytz.timezone("EST").localize(
                    dt.datetime.now() - dt.timedelta(days=365)):
                n = j
                break
        existing_df = existing_df[n:]

    else:
        existing_data = False
        f.write(f"Creating new Reddit data...' \n")
        print('Creating new Reddit data...')

    f.close()

    # clear/create out_file for rewriting
    # unnecessary if using shell cmds, just write to file
    g = open(str(out_file), 'w+')
    g.close()

    if existing_data:
        print("Rewriting old file")
        start_time = time.time()
        existing_df.to_csv(out_file, index=False)
        print(f"Took {time.time() - start_time} time to rewrite old file")


    while last_page != []:

        start_time = time.time()
        print(f"Crawling Page {i + 1}")

        if existing_data:
            last_page = crawl_page(subreddit, last_page=last_page, after=int(str_date.timestamp()))
        else:
            last_page = crawl_page(subreddit, last_page=last_page)

        submissions += last_page

        # Pause to not overload API with requests
        time.sleep(3)

        if last_page == []:
            break

        df = pd.DataFrame(last_page)
        _timestamp = df["created_utc"].apply(get_date)
        new_df = df.assign(created_utc=_timestamp)
        final_df = new_df[["id", "created_utc", "selftext", "title"]]

        if i == 0 and not existing_data:
            final_df.to_csv(out_file, index=False)
        else:
            final_df.to_csv(out_file, mode='a', header=False, index=False)

        i += 1
        delta = time.time() - start_time
        print(f"Took {delta} time to crawl page")
        final_time = last_page[-1]["created_utc"]
        print(f"Last timestamp of crawled page: {final_time}")

    return submissions


if __name__ == "__main__":
    latest_submissions = crawl_subreddit("wallstreetbets")