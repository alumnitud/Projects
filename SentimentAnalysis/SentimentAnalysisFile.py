from textblob import TextBlob

txtfiles= [
    'NegativeText.txt', 
    'NeutralText.txt', 
    'PositiveText.txt']

for txt in txtfiles:
    with open(txt, 'r') as f:
        text= f.read()
        blob= TextBlob(text)
        sentiment = blob.sentiment.polarity # -1 to 1
        print(sentiment)

    