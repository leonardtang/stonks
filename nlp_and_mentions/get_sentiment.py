import pathlib
import time
import pandas as pd
import datetime as dt

# from scipy.ndimage import gaussian_gradient_magnitude
from helpers import preprocess_wsb_df, nested_dict, strip_last_line
from expertai.nlapi.cloud.client import ExpertAiClient

client = ExpertAiClient()
language = 'en'


def get_wsb_text_today():
    """
    Get WSB text data from today.
    """

    df = pd.read_csv('data/wsb_submissions.csv',
                     parse_dates=["created_utc"],
                     engine='python',
                     encoding='utf-8',
                     error_bad_lines=False)
    date_df = preprocess_wsb_df(df)
    unique_dates = date_df.created_utc.unique()
    daily_df = date_df[date_df["created_utc"].isin(pd.date_range(unique_dates[-1], unique_dates[-1]))]
    daily_df.to_csv('data/wsb_daily_text.csv')

    return daily_df


def predict_sentiment(input_text):
    output = client.specific_resource_analysis(body={"document": {"text": input_text}},
                                               params={'language': language, 'resource': 'sentiment'})

    return output.sentiment.overall


def summarize_daily_sentiment(date, save_summary=True):
    """
    Calculate percentage of positive posts for a given date as well as
    average sentiment value across posts.
    """

    historical_df = pd.read_csv('data/processed_wsb_submissions.csv')
    historical_df["created_utc"] = pd.to_datetime(historical_df["created_utc"])
    daily_df = historical_df[historical_df["created_utc"].isin([date])]
    text_column = daily_df['text']

    positive_counts = 0
    average_sentiment = 0
    valid_posts = 0

    for i, text in text_column.iteritems():
        if i % 20 != 0:
            continue

        try:
            sentiment_score = predict_sentiment(text)
            if sentiment_score > 0:
                positive_counts += 1

        except Exception:
            print(Exception)
            pass

        else:
            average_sentiment += sentiment_score
            valid_posts += 1

    if valid_posts == 0:
        return None, None

    percentage_positive = positive_counts / valid_posts
    average_sentiment = average_sentiment / valid_posts

    if save_summary:
        f = open("data/sentiment_percentage.txt", "w")
        f.write(str(percentage_positive))
        f = open("data/average_sentiment.txt", "w")
        f.write(str(average_sentiment))

    return percentage_positive, average_sentiment


def get_historical_sentiment():
    historical_dates_df = pd.read_csv('data/processed_wsb_submissions.csv')
    historical_dates_df["created_utc"] = pd.to_datetime(historical_dates_df["created_utc"])

    unique_dates = historical_dates_df.created_utc.unique()

    f = open("sentiment_checkpoint.txt", "w")

    historical_sentiment = nested_dict()

    OUT_FILE = pathlib.Path('data/historical_sentiment.csv')
    if OUT_FILE.exists():
        existing_data = True
        existing_df = pd.read_csv(OUT_FILE)
        str_last_recorded_sent_date = existing_df["Unnamed: 0"].iloc[-1]
        # last_recorded_date = dt.datetime.strptime(str_last_recorded_date, '%Y-%m-%d')
        print(f'Last recorded sentiment date: {str_last_recorded_sent_date}')
        print('Appending to existing sentiment data...')

        n = 0
        for j in existing_df.index:
            if pd.to_datetime(existing_df.loc[j]["Unnamed: 0"]) >= dt.datetime.now() - dt.timedelta(days=365):
                n = j
                break

        existing_df = existing_df[n:]

    else:
        existing_data = False
        print('Creating new sentiment data...')

    f.close()

    if existing_data:
        print("Rewriting old file")
        start_time = time.time()
        existing_df.to_csv(OUT_FILE, index=False)
        strip_last_line(str(OUT_FILE))
        print(f"Took {time.time() - start_time} time to rewrite old file")
        datetime_last_recorded_date = pd.to_datetime(str_last_recorded_sent_date)

    for i, date in enumerate(unique_dates):

        date = date.astype('datetime64[us]').astype(dt.datetime)

        if existing_data:
            if date < datetime_last_recorded_date:
                continue

        print(f'Summarizing sentiment for date: {date}')

        # Log the most recent cleaned date to resume cleaning from in the event that your machine dies, restarts, etc.
        f = open("stock_checkpoint.txt", "a")
        print(f"Getting sentiment for {date}")
        f.write(f"Getting sentiment for {date} \n")
        start = time.time()

        # Most recent WSB page
        if i == len(unique_dates) - 1:
            summarize_daily_sentiment(date, save_summary=True)

        pos_percent, avg_sent = summarize_daily_sentiment(date, save_summary=False)

        historical_sentiment[date]['percentage_positive'] = pos_percent
        historical_sentiment[date]['average_sentiment'] = avg_sent

        historical_sent_df = pd.DataFrame.from_dict(historical_sentiment, orient='index')

        print(f'Percentage Positive: {pos_percent}')
        print(f'Average Sentiment: {avg_sent}')

        delta = time.time() - start
        print(f"Compute Time: {delta}")
        f.write(f"Compute Time: {delta} \n\n")
        f.close()

        if i == 50:
            if not existing_data:
                historical_sent_df.to_csv(OUT_FILE)
        
    if existing_data:
        historical_sent_df.to_csv(OUT_FILE, mode='a', header=False)
    else:
        historical_sent_df.to_csv(OUT_FILE)


if __name__ == "__main__":
    get_historical_sentiment()
