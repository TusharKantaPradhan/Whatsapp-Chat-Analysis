import pandas as pd
import numpy as np
import re
from collections import Counter
import emoji
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import seaborn as sns

def extract_emojis(s: str):
    if not isinstance(s, str):
        return []
    return [c for c in s if c in emoji.UNICODE_EMOJI_ENGLISH]

def basic_stats(df: pd.DataFrame):
    total_msgs = len(df)
    total_words = df['message'].dropna().apply(lambda s: len(str(s).split())).sum()
    total_media = df['message'].str.contains('<Media omitted>|<Media omitted>').sum()
    participants = df['author'].dropna().unique().tolist()
    return {
        "total_messages": int(total_msgs),
        "total_words": int(total_words),
        "total_media_messages": int(total_media),
        "participants": participants
    }

def sentiment_analysis(df: pd.DataFrame):
    # compute polarity & subjectivity
    df = df.copy()
    df['text'] = df['message'].fillna('')
    df['polarity'] = df['text'].apply(lambda t: TextBlob(t).sentiment.polarity)
    df['subjectivity'] = df['text'].apply(lambda t: TextBlob(t).sentiment.subjectivity)
    return df[['datetime','author','message','polarity','subjectivity']]

def top_words(df: pd.DataFrame, top_n=30, remove_stopwords=True):
    text = " ".join(df['message'].dropna().astype(str).tolist()).lower()
    # remove urls and mentions
    text = re.sub(r'http\S+','', text)
    tokens = re.findall(r'\b\w+\b', text)
    stop = set(STOPWORDS) if remove_stopwords else set()
    tokens = [t for t in tokens if t not in stop and len(t)>1]
    c = Counter(tokens)
    return c.most_common(top_n)

def emoji_trends(df: pd.DataFrame, top_n=20):
    emojis = df['message'].dropna().apply(extract_emojis).sum()
    c = Counter(emojis)
    return c.most_common(top_n)

def generate_wordcloud(df: pd.DataFrame, output_path=None):
    text = " ".join(df['message'].dropna().astype(str).tolist())
    wc = WordCloud(width=800, height=400, collocations=False).generate(text)
    if output_path:
        wc.to_file(output_path)
    return wc

def messages_per_hour(df: pd.DataFrame):
    df = df.copy()
    df['hour'] = df['datetime'].dt.hour
    return df.groupby('hour').size()

def messages_per_day(df: pd.DataFrame):
    df = df.copy()
    df['date'] = df['datetime'].dt.date
    return df.groupby('date').size()
