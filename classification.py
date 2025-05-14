import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('mental_health_posts.csv')

def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity == 0:
        return "Neutral"
    else:
        return "Negative"

df = df.dropna()

df['Sentiment'] = df['Content'].apply(get_sentiment)


high_risk_terms = [
    "i don’t want to be here", "end my life", "can’t go on", 
    "no reason to live", "suicidal", "give up", "hopeless"
]

moderate_terms = [
    "feeling lost", "struggling", "need help", "can’t cope",
    "overwhelmed", "depressed", "seeking advice"
]


def classify_risk(text):
    text = text.lower()
    for phrase in high_risk_terms:
        if phrase in text:
            return "High-Risk"
    for phrase in moderate_terms:
        if phrase in text:
            return "Moderate Concern"
    return "Low Concern"

df['Risk_Level'] = df['Content'].apply(classify_risk)

'''
helps identify which words are most unique/relevant/important in each post
high TF-IDF scores = distress
'''
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['Content'])


plt.figure(figsize=(8,5))
sns.countplot(x=df['Sentiment'], palette="coolwarm")
plt.title("Sentiment Distribution")
plt.show()


plt.figure(figsize=(8,5))
sns.countplot(x=df['Risk_Level'], palette="viridis")
plt.title("Risk Level Distribution")
plt.show()


df.to_csv("classified_mental_health_posts.csv", index=False)

