import os
import pandas as pd
import numpy as np
import redditcleaner
from collections import defaultdict


def clean_ticker_list(og_tickers):
    """
    Filters ticker list for intentional ticker mentions, excluding common
    acronyms and words that also happen to be ticker symbols.
    """

    print('Cleaning Tickers List...')
    stop_tickers = {'LOL', 'BMW', 'BUT', 'EOD', 'DJIA', 'ROFL',
                    'F', 'HQ', 'LMFAO', 'CEO', 'ATH', 'CTO', 'L',
                    'OP', 'STILL', 'FL', 'X', 'TOS', 'IV', 'PDFUA',
                    'YOLO', 'GDP', 'CFO', 'BEZOS', 'TYS', 'AYYMD',
                    'S', 'E', 'FEB', 'OK', 'NOV', 'ICE', 'ER',
                    'MACD', 'FIFA', 'COD', 'LMAO', 'USA', 'SEC',
                    'BTFD', 'GOD', 'DOWAM', 'WTF', 'RISEIPA',
                    'SEPT', 'A', 'JUL', 'DD', 'EDIT', 'ELON', 'G',
                    'LPT', 'PRAY', 'SEP', 'AT', 'DOJ', 'CA', 'GG',
                    'FD', 'V', 'RIP', 'PR', 'D', 'I', 'DR', 'FOMO',
                    'NOT', 'FBI', 'MILF', 'USD', 'BE', 'FDA', 'IMO',
                    'IS', 'C', 'AH', 'ITM', 'U', 'EZ', 'SSN', 'Y',
                    'RAW', 'US', 'PS', 'O', 'H', 'RH', 'POS', 'Q',
                    'WSB', 'JAN', 'URL', 'T', 'IPO', 'B', 'IL', 'KYS',
                    'PT', 'LGMA', 'ISIS', 'CPU', 'TICK', 'TL', 'RED',
                    'ATM', 'N', 'P', 'GOAT', 'EV', 'OTM', 'AUG', 'J',
                    'TL;DR', 'R', 'Z', 'IT', 'W', 'DEC', 'PUMP', 'PC',
                    'PM', 'M', 'OCT', 'K'}
    stock_tickers = list(filter(lambda x: x not in stop_tickers, og_tickers))
    return stock_tickers


def preprocess_wsb_df(df: pd.DataFrame):
    """
    Squashes together body and text, and changes all DateTimes to be dates
    """

    print('Preprocessing WSB Data...')
    df = df.replace(np.nan, '', regex=True)
    df = df.replace({'\[removed\]': ''}, regex=True)

    df['selftext'] = df['selftext'].map(redditcleaner.clean)
    df['title'] = df['title'].map(redditcleaner.clean)

    df['text'] = df.selftext.astype(str).str.cat(df.title.astype(str), sep='. ')
    df = df.drop(columns=["selftext", "title"])

    date_df = df.copy()
    date_df["created_utc"] = pd.to_datetime(df['created_utc'], utc=True)
    date_df["created_utc"] = date_df["created_utc"].dt.date.astype("datetime64")

    return date_df


def strip_last_line(f_name):
    with open(f_name, "r+", encoding="utf-8") as f:
        f.seek(0, os.SEEK_END)

        pos = f.tell() - 2

        while pos > 0 and f.read(1) != '\n':
            pos -= 1
            f.seek(pos, os.SEEK_SET)

        if pos > 0:
            f.seek(pos + 1, os.SEEK_SET)
            f.truncate()


def inner_dict():
    return {}


def nested_dict():
    return defaultdict(inner_dict)


nltk_stopwords = {'HERS', 'NO', 'AREN', "SHOULD'VE", 'WOULDN', "AREN'T", 'DOESN', 'THEIR',
                  "THAT'LL", 'WITH', 'MIGHTN', 'MOST', 'THEIRS', 'FEW', 'HASN', 'WHAT', 'SHAN',
                  'NEEDN', 'ONE', 'LL', 'NOT', 'HAVE', 'HERE', "YOU'LL", 'OURS', "YOU'RE", 'AFTER',
                  'THIS', 'THEM', 'AS', "COULDN'T", 'WEREN', 'IT', "WON'T", 'SHOULD', 'THOSE',
                  'WHICH', 'BELOW', "WASN'T", 'NEXT', 'INTO', 'WASN', 'HADN', 'DOES', 'DOWN', 'IN',
                  'ON', 'ONCE', 'THERE', 'MORE', 'THAN', 'M', 'MA', 'WE', 'DID', 'ISN', 'THROUGH',
                  'THESE', 'IS', 'OTHER', 'YOURS', 'OF', "SHE'S", 'DOING', 'THE', 'ABOVE', 'DO', 'HOW',
                  'WON', 'D', 'OFF', 'SO', 'UNDER', 'BUT', "IT'S", 'HAD', 'BIG', 'OWN', "DIDN'T",
                  'FURTHER', "HAVEN'T", 'OUR', 'VERY', 'IF', 'SUCH', 'T', 'LOVE', 'O', 'WHY', 'HAVEN',
                  "WOULDN'T", 'HERSELF', 'FROM', 'WHEN', 'DON', 'BY', "HASN'T", 'HIM', 'ARE', 'NOW',
                  'MUSTN', 'MYSELF', 'CAN', 'MY', 'DURING', 'UNTIL', "SHAN'T", 'WHILE', 'NEW', 'AM',
                  'ANY', 'I', 'WHERE', 'OVER', 'VE', "WEREN'T", 'GO', 'SHOULDN', "MIGHTN'T", 'S',
                  'HER', 'AN', 'TO', 'AIN', 'SEE', "YOU'VE", 'ABOUT', 'THEMSELVES', "SHOULDN'T",
                  'JUST', 'HE', 'OUT', 'YOURSELF', 'WERE', 'BEING', 'THAT', 'AND', 'COULDN',
                  "DOESN'T", 'OURSELVES', 'WHOM', 'RE', 'BECAUSE', 'ITS', 'SOME', 'DIDN', "YOU'D",
                  'HAS', 'Y', 'TOO', 'OR', 'YOU', 'YOURSELVES', 'EACH', 'A', 'AGAIN', "DON'T", 'TD',
                  'AGAINST', 'BEEN', "HADN'T", 'SHE', 'BE', 'YOUR', 'HIS', 'HIMSELF', 'AI', "ISN'T",
                  'ITSELF', 'THEY', 'BOTH', 'BEFORE', 'UP', 'HAVING', 'WAS', 'FOR', 'ALL', "MUSTN'T",
                  'WHO', 'NOR', 'ME', 'WILL', 'SAME', 'BETWEEN', 'AT', 'ONLY', 'THEN', "NEEDN'T"}


if __name__ == "__main__":
    print(nltk_stopwords)