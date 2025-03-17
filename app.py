import requests
from bs4 import BeautifulSoup
import random
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from translate import Translator
import os
import streamlit as st
from yake import KeywordExtractor
from gtts import gTTS
from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Usage
tts = gTTS(text="Hello", lang='en')

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()


# Function to extract news
def extract_news(company_name):
    rss_url = f"https://news.google.com/rss/search?q={company_name}"
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    ]
    
    headers = {"User-Agent": random.choice(user_agents)}
    
    try:
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        
        articles = []
        for item in soup.find_all("item")[:10]:
            title = item.find("title").text if item.find("title") else "No title found"
            
            summary_content = item.find("description").text if item.find("description") else "Unknown summary"
            summary_soup = BeautifulSoup(summary_content, "html.parser")
            
            link_element = summary_soup.find("a")
            link = link_element["href"] if link_element and "href" in link_element.attrs else "No link found"
            
            summary = summary_soup.get_text()
            
            articles.append({
                "title": title,
                "link": link,
                "summary": summary
            })
        
        return articles
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

# Function for sentiment analysis
def sentiment_analysis(text):
    sentiment = sia.polarity_scores(text)
    
    if sentiment['compound'] > 0.05:
        return "Positive"
    elif sentiment['compound'] < -0.05:
        return "Negative"
    else:
        return "Neutral"

# Function for comparative analysis
def comparative_analysis(articles):
    sentiments = [sentiment_analysis(article['summary']) for article in articles]
    
    positive_count = sentiments.count("Positive")
    negative_count = sentiments.count("Negative")
    neutral_count = sentiments.count("Neutral")
    
    return {
        "Positive": positive_count,
        "Negative": negative_count,
        "Neutral": neutral_count
    }

def extract_topics(summary):
    extractor = KeywordExtractor()
    keywords = extractor.extract_keywords(summary)
    return [keyword[0] for keyword in keywords]

# Function for text-to-speech conversion
def text_to_speech_hindi(text):
    translator = Translator(to_lang="hi")
    hindi_text = translator.translate(text)
    
    tts = gTTS(text=hindi_text, lang='hi')
    tts.save("output.mp3")

# Main application
def main():
    st.title("News Sentiment Analysis Tool")
    company_name = st.text_input("Enter Company Name")
    
    if st.button("Fetch News"):
        articles = extract_news(company_name)
        
        output_data = {
            "Company": company_name,
            "Articles": [],
            "Comparative Sentiment Score": {
                "Sentiment Distribution": {},
                "Coverage Differences": [],
                "Topic Overlap": {
                    "Common Topics": [],
                    "Unique Topics": {}
                }
            },
            "Final Sentiment Analysis": "",
            "Audio": "[Play Hindi Speech]"
        }
        
        topics_per_article = {} # Store topics for each article
        
        for i, article in enumerate(articles, 1):
            st.write(f"Article {i}:")
            st.write(f"Title: {article['title']}")
            st.write(f"Link: {article['link']}")
            st.write(f"Summary: {article['summary']}")
            st.write(f"Sentiment: {sentiment_analysis(article['summary'])}")
            
            topics = extract_topics(article['summary'])
            st.write(f"Topics: {topics}")
            st.write("")
            
            topics_per_article[i] = topics # Store topics

            output_data["Articles"].append({
                "Title": article['title'],
                "Summary": article['summary'],
                "Sentiment": sentiment_analysis(article['summary']),
                "Topics": topics
            })
                
        sentiments = comparative_analysis(articles)
        output_data["Comparative Sentiment Score"]["Sentiment Distribution"] = sentiments
        
       

        # Topic Overlap
        all_topics = set()
        for topics in topics_per_article.values():
            all_topics.update(topics)

        common_topics = []
        for topic in all_topics:
            count = sum(topic in article_topics for article_topics in topics_per_article.values())
            if count > 1:
                common_topics.append((topic, count))

        output_data["Comparative Sentiment Score"]["Topic Overlap"]["Common Topics"] = [topic for topic, count in common_topics]

        # Unique Topics
        unique_topics = {}
        for i in range(1, len(articles) + 1):
            other_topics = set()
            for j in range(1, len(articles) + 1):
                if i != j:
                    other_topics.update(topics_per_article[j])
            unique_topics[f"Article {i}"] = list(set(topics_per_article[i]) - other_topics)
        output_data["Comparative Sentiment Score"]["Topic Overlap"]["Unique Topics"] = unique_topics
        
        if sentiments["Positive"] > sentiments["Negative"]:
            final_sentiment = f"{company_name}'s latest news coverage is mostly positive. Potential stock growth expected."
        else:
            final_sentiment = f"{company_name}'s latest news coverage is mostly negative. Potential stock decline expected."
        
        output_data["Final Sentiment Analysis"] = final_sentiment
        
        st.write(final_sentiment)
        
        # Convert Final Sentiment to Audio
        text_to_speech_hindi(final_sentiment)
        
        st.write("Output Data:")
        st.write(output_data)
        
        st.audio("output.mp3")

if __name__ == "__main__":
    main()