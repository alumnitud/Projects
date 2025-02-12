import tkinter as tk # for GUI
import nltk # for natural language processing
from textblob import TextBlob # for sentiment analysis
from newspaper import Article # for scraping news articles

def summarize():
    url= urltext.get("1.0", "end").strip() # get the url from the user input, strip() removes any leading or trailing spaces, get the text from the first character to the end

    # Summarization of the news articles
    article = Article(url)
    article.download()
    article.parse() #parse the article in parts it needs
    article.nlp() #natural language processing

    # For sentiment analysis we need to convert the article into a textblob object
    analysis= TextBlob(article.text) # we are doing this with whole text but also possible with summary
    sentimentscore= analysis.polarity

    #add the data to the relevant text fields

    title.config(state="normal") # to make the text field editable
    author.config(state="normal") # to make the text field editable
    pubDate.config(state="normal") # to make the text field editable
    summary.config(state="normal") # to make the text field editable
    sentiment.config(state="normal") # to make the text field editable

    title.delete('1.0', 'end') # delete the previous content
    title.insert('1.0', article.title) # insert the new content
    author.delete('1.0', 'end') # delete the previous content
    author.insert('1.0', article.authors) # insert the new content
    pubDate.delete('1.0', 'end') # delete the previous content
    pubDate.insert('1.0', str(article.publish_date)) # insert the new content
    summary.delete('1.0', 'end') # delete the previous content
    summary.insert('1.0', article.summary) # insert the new content
    sentiment.delete('1.0', 'end') # delete the previous content
    sentiment.insert('1.0', f'Sentiment Score: {sentimentscore}, Sentiment: {"positive" if sentimentscore > 0 else "negative" if sentimentscore < 0 else "neutral"}') # insert the new content   

    title.config(state="disabled") # to make the text field non-editable
    author.config(state="disabled") # to make the text field non-editable
    pubDate.config(state="disabled") # to make the text field non-editable
    summary.config(state="disabled") # to make the text field non-editable
    sentiment.config(state="disabled") # to make the text field non-editable

    
# GUI
root= tk.Tk()
root.title("News Summarizer")
root.geometry("1200x600") # width x height

tlabel= tk.Label(root, text="Title")
tlabel.pack()

title= tk.Text(root, height=1, width= 140)
title.config(state="disabled", bg='#dddddd') # so user cannot edit or give input
title.pack()

alabel= tk.Label(root, text="Author")
alabel.pack()

author= tk.Text(root, height=1, width= 140)
author.config(state="disabled", bg='#dddddd') # so user cannot edit or give input
author.pack()

plabel= tk.Label(root, text="Publication Date")
plabel.pack()

pubDate= tk.Text(root, height=1, width= 140)
pubDate.config(state="disabled", bg='#dddddd') # so user cannot edit or give input
pubDate.pack()

slabel= tk.Label(root, text="Summary")
slabel.pack()

summary= tk.Text(root, height=20, width= 140)
summary.config(state="disabled", bg='#dddddd') # so user cannot edit or give input
summary.pack()

sentlabel= tk.Label(root, text="Sentiment")
sentlabel.pack()

sentiment= tk.Text(root, height=1, width= 140)
sentiment.config(state="disabled", bg='#dddddd') # so user cannot edit or give input
sentiment.pack()

urllabel= tk.Label(root, text="URL")
urllabel.pack()

urltext= tk.Text(root, height=1, width= 140) #url is not disabled as user has to give input
urltext.pack()

btn= tk.Button(root, text="Summarize", command= summarize) # defining a button and the function which defines its functionality
btn.pack()

root.mainloop() # to keep the window open