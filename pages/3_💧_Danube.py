import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

# Step 1: Scrape the Articles
base_url = "https://www.heute.at/s"
search_query = "donau" # for danube river
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"
}

# Fetch the search results page
response = requests.get(f"{base_url}/suchen?q={search_query}", headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract article contents (based on the website's structure at the time of writing; may change over time)
article_texts = []
articles = soup.find_all('div', class_='story')  # Assuming 'story' class represents an article

for article in articles:
    article_text = article.get_text()
    article_texts.append(article_text)

# Combine all the articles into one string
text_combined = ' '.join(article_texts)

# Step 2: Create a Word Cloud
wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=set(['die', 'der', 'und']), min_font_size=10).generate(text_combined)

# Display the Word Cloud with Streamlit
st.write("# Word Cloud for Articles on Danube River from heute.at")
st.pyplot(wordcloud.to_image())