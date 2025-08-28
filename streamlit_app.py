import streamlit as st
import pandas as pd
from scripts.chat_parser import parse_chat
from scripts.analysis import sentiment_analysis, word_frequency, emoji_analysis
from scripts.visuals import plot_wordcloud, plot_sentiment_trend, plot_emoji_usage

st.title('📊 WhatsApp Chat Analysis')

uploaded_file = st.file_uploader('Upload WhatsApp chat (.txt)', type=['txt'])

if uploaded_file:
    chat_df = parse_chat(uploaded_file)
    st.write('Sample messages:', chat_df.head())

    st.subheader('Word Frequency')
    wf = word_frequency(chat_df)
    st.bar_chart(wf.head(20).set_index('word'))

    st.subheader('Sentiment Trend')
    st.pyplot(plot_sentiment_trend(chat_df))

    st.subheader('Emoji Usage')
    st.pyplot(plot_emoji_usage(chat_df))

    st.subheader('Word Cloud')
    st.pyplot(plot_wordcloud(chat_df))
