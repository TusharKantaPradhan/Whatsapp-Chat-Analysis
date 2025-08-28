import matplotlib.pyplot as plt
from wordcloud import WordCloud
from .analysis import sentiment_analysis, emoji_analysis

def plot_wordcloud(df):
    text = ' '.join(df['message'])
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10,6))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    return fig

def plot_sentiment_trend(df):
    df = sentiment_analysis(df)
    fig, ax = plt.subplots(figsize=(10,6))
    df['sentiment'].rolling(50).mean().plot(ax=ax)
    ax.set_title('Sentiment Trend')
    return fig

def plot_emoji_usage(df):
    emojis = emoji_analysis(df).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    ax.bar(emojis['emoji'], emojis['count'])
    ax.set_title('Top Emoji Usage')
    return fig
