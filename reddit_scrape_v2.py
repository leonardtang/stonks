import sys
from datetime import datetime, timedelta
from pprint import pprint
import praw
import logging
import pandas as pd
import pytz
import datetime as dt

logger = logging.getLogger("INFO")

user_agent = "HFAC-Quant"
r = praw.Reddit(client_id='8duVCOaxlCUXSg',
                client_secret='gOvemI6ewhctQUdBzi9Dt_6c69Z92w',
                user_agent='HFAC-Comp',
                username='leonardtang',
                password='chipismonk2')


class SubredditLatest(object):
    """Get all available submissions within a subreddit newer than x."""

    def __init__(self, subreddit, dt):

        # master list of all available submissions
        self.total_list = []

        # subreddit must be a string of the subreddit name (e.g., "soccer")
        self.subreddit = subreddit

        # dt must be a utc datetime object
        self.dt = dt

    # def __call__(self):
    #     self.get_submissions(self)
    #     return self.total_list

    def get_submissions(self, paginate=False):
        """Get limit of subreddit submissions."""
        limit = 100  # Reddit maximum limit

        if paginate is True:
            try:
                # get limit of items past the last item in the total list
                submissions = r.subreddit(self.subreddit).new(limit=limit,
                                                              params={"after": self.total_list[-1].fullname})
            except IndexError:
                logger.exception("param error")
                return
        else:
            submissions = r.subreddit(self.subreddit).new(limit=limit)

        submissions_list = [
            # iterate through the submissions generator object
            x for x in submissions
            # add item if item.created_utc is newer than an hour ago
            if datetime.utcfromtimestamp(x.created_utc) >= self.dt
        ]
        self.total_list += submissions_list

        # if you've hit the limit, recursively run this function again to get
        # all of the available items
        if len(submissions_list) == limit:
            self.get_submissions(paginate=True)
        else:
            return


def get_date(created):
    # utc = pytz.utc
    # est = pytz.timezone('US/Eastern')
    utc_dt = datetime.utcfromtimestamp(created).replace(tzinfo=pytz.utc)
    tz = pytz.timezone('America/New_York')
    est_dt = utc_dt.astimezone(tz)
    return est_dt


if __name__ == '__main__':
    an_hour_ago = datetime.utcnow() - timedelta(hours=3)
    # since = 1420088400
    latest = SubredditLatest("wallstreetbets", an_hour_ago)
    latest.get_submissions()
    pprint(latest.total_list)

    topics_dict = {"title": [],
                   "score": [],
                   "id": [], "url": [],
                   "comms_num": [],
                   "created": [],
                   "body": []}

    for submission in latest.total_list:
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext)

    topics_data = pd.DataFrame(topics_dict)
    # _timestamp = topics_data["created"].apply(get_date)
    # topics_data = topics_data.assign(created=_timestamp)
    pprint(topics_data)

    topics_data.to_csv("reddit_scrape_v2.csv")

    # flagged_words = ["YOLO", "PUMP", "RH", "EOD", "IPO", "ATH", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
    #                 "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
