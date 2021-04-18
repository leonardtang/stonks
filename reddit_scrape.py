import warnings
import requests
import time
import pandas as pd
import pytz
import datetime as dt
from urllib3.exceptions import ProtocolError
from ratelimiter import RateLimiter

url = "https://api.pushshift.io/reddit/search/submission"

"""Eventually, have some code that continuously runs and checks pulled results with existing CSV and writes new lines 
"""

######## RESET TIME STAMP!!!!!

def crawl_page(subreddit: str, last_page=None):
    if last_page is None:
        params = {"subreddit": subreddit,
                  "size": 500,
                  "sort": "desc",
                  "sort_type": "created_utc",
                  "before": 1612193357,
                  "stream": True}

    else:
        params = {"subreddit": subreddit,
                  "size": 500,
                  "sort": "desc",
                  "sort_type": "created_utc",
                  "stream": True}

    # Keep crawling subreddit until no more pages
    if last_page is not None:
        if len(last_page) > 0:
            params["before"] = last_page[-1]["created_utc"]
        else:
            return []

    try:
        with requests.get(url, params) as results:
            if not results.ok:
                potential_error = True
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
    # utc = pytz.utc
    est = pytz.timezone('US/Eastern')
    return dt.datetime.fromtimestamp(created, tz=est)


def crawl_subreddit(subreddit, max_submissions=None):
    submissions = []
    last_page = None
    i = 0
    while last_page != []:
        start_time = time.time()
        print(f"Crawling Page {i + 1}")
        last_page = crawl_page(subreddit, last_page)
        submissions += last_page
        # Pause to not overload API with requests
        time.sleep(3)

        df = pd.DataFrame(last_page)
        _timestamp = df["created_utc"].apply(get_date)
        new_df = df.assign(created_utc=_timestamp)
        final_df = new_df[["id", "created_utc", "selftext", "title"]]
        # if i == 0:
        #     final_df.to_csv("wsb_fresh_topics.csv", index=False)
        # else:
        final_df.to_csv("wsb_fresh_topics.csv", mode='a', header=False, index=False)

        i += 1
        delta = time.time() - start_time
        print(f"Took {delta} time to crawl page")
        final_time = last_page[-1]["created_utc"]
        print(f"Last timestamp of crawled page: {final_time}")

    return submissions


# rate_limiter = RateLimiter(max_calls=30, period=1)
# with rate_limiter:
latest_submissions = crawl_subreddit("wallstreetbets")

df = pd.DataFrame(latest_submissions)
_timestamp = df["created_utc"].apply(get_date)
new_df = df.assign(created_utc=_timestamp)

final_df = new_df[["id", "created_utc", "selftext", "title"]]
final_df.to_csv("wsb_fresh_topics_with_stream.csv", index=False)
