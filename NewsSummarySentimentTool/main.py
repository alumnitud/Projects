import tkinter as tk # for GUI
import nltk # for natural language processing
from textblob import TextBlob # for sentiment analysis
from newspaper import Article # for scraping news articles

# Summarization of the news articles

url = 'https://www.bbc.com/news/articles/c3vp06k90d5o'

article = Article(url)
article.download()
article.parse() #parse the article in parts it needs
article.nlp() #natural language processing

print(f'Title: {article.title}')
print(f'Authors: {article.authors}')
print(f'Publication Date: {article.publish_date}')  
print(f'Summary: {article.summary}')

# For sentiment analysis we need to convert the article into a textblob object
analysis= TextBlob(article.text) # we are doing this with whole text but also possible with summary
sentiment= analysis.sentiment.polarity # -1 to 1
print(sentiment)
print(f'Sentiment: {"positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral"}')    