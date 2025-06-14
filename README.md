﻿# Ethiopian Banking App Reviews
 Customer Experience Analytics for Fintech Apps
Overview
This project focuses on analyzing customer satisfaction for mobile banking apps by scraping and analyzing user reviews from the Google Play Store for three Ethiopian banks: CBE, BOA, and Dashen Bank. It encompasses web scraping, sentiment analysis, and data visualization to simulate the role of a Data Analyst at Omega Consultancy.

Objectives

Scrape User Reviews: Collect and preprocess reviews from Google Play.
Analyze Sentiment: Determine sentiment (positive/negative/neutral) and extract key themes.
Identify Insights: Highlight satisfaction drivers and pain points.
Store Data: Implement a relational database in Oracle.
Deliver Recommendations: Provide actionable insights through visualizations.
Key Features

Web Scraping: Utilize google-play-scraper to gather 400+ reviews per bank.
Sentiment Analysis: Employ distilbert-base-uncased-finetuned-sst-2-english for sentiment scoring.
Thematic Analysis: Extract keywords and cluster themes using NLP techniques.
Database Implementation: Design and populate an Oracle database with cleaned data.
Visual Reporting: Create visualizations to present findings effectively.
Installation

pip install google-play-scraper
pip install pandas
pip install transformers
Usage
Scraping Reviews:

run:
from google_play_scraper import reviews
result, continuation_token = reviews('com.nianticlabs.pokemongo', lang='en', country='us')
Sentiment Analysis:

run:
from transformers import pipeline
sentiment_analyzer = pipeline("sentiment-analysis")
scores = sentiment_analyzer("This app is great!")
Data Storage:
Set up an Oracle database and define schema for the reviews and banks.

Contribution
Contributions are welcome! Please submit a pull request or open an issue for any improvements or bug fixes.
