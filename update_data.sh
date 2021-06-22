#!/bin/bash
source venv/bin/activate

python scrapers/reddit_scrape.py
python nlp_and_mentions/get_stock_mentions.py
python nlp_and_mentions/get_crypto_mentions.py
python scrapers/yahoo_scrape.py
python nlp_and_mentions/get_market_volume.py
python nlp_and_mentions/get_sentiment.py
python nlp_and_mentions/extract_keywords.py
python upload_s3.py

# TODO: upload CSVs to S3 as part of update.