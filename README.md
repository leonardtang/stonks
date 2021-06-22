## Inspiration

In the context of the recent retail investor craze, I decided to investigate how informative a popular retail investing forum on Reddit, r/WallStreetBets, could actually be for choosing investments.

## What it does

I encourage you to browse the site. It is a one-stop dashboard for understanding the engima that is r/WallStreetBets.

Namely, it provides sentiment features extracted from user comments alongside stock/cryptocurrency prices, volatility, and other key metrics. 

## How we built it

I used the Pushshift.io API to grab the Reddit data and yahoo-finance-2 to get the pricing data. I threw everything in a tmux shell since this was _relatively big_ data (on the order of millions of rows).

The ExpertAI API makes it a breeze to perform NLP tasks. I used it to extract keyphrases from Reddit comments and analyze user sentiment over time.

The frontend of the website was built with Dash (Plotly), HTML, and CSS. It's hosted on Heroku at the moment.

## Challenges we ran into

Much like the Twitter API, the Reddit API is garbage. It limits you to the 1000 most recent listings by time – truly unfortunate. However, the Pushshift.io API is not perfect either; its connection is tenuous at best. I implemented continuous re-requesting to ensure that I would eventually get the data.

Too, I had trained some transformer models to do the required sentiment analysis tasks, but such state-of-the-art models cannot quite fit extremely long text in memory (in the same vein as catastrophic forgetting), and as such their power greatly diminishes. Fortunately, the folks at ExpertAI appear to have solved this problem, so I used their API instead.

## Accomplishments that we're proud of

The site looks stellar; the information is useful; the vibes are good.

## What's next for StOnKs

I want to migrate everything to AWS. I have a Lambda function set up that runs an EC2 instance to update the data in S3, but it is not yet incorporated into the app itself. It would take ~15 minutes to tie everything together.
