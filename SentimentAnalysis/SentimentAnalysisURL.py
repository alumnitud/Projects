from textblob import TextBlob
from newspaper import Article

urls= [
    'https://en.wikipedia.org/wiki/Artificial_intelligence',
    'https://www.thehindu.com/news/national/mumbai-police-registers-case-against-ranveer-allahbadia/article69210369.ece',
    'https://economictimes.indiatimes.com/news/international/global-trends/nasa-spacex-capsule-switch-poised-to-bring-starliner-astronauts-home-days-sooner/articleshow/118160520.cms?from=mdr'
]

for url in urls:
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    text= article.summary

    blob= TextBlob(text)
    sentiment = blob.sentiment.polarity # -1 to 1
    print (f"Sentiment for {url} is {sentiment}\n")
#print (text)


