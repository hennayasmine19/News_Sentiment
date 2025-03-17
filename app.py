import streamlit as st
import requests

# Streamlit App UI
st.set_page_config(page_title="News Sentiment Analysis", layout="wide")

# Title
st.title("📰 News Sentiment Analysis & Hindi Text-to-Speech")

# User input
st.sidebar.header("Enter a Company Name")
company_name = st.sidebar.text_input("Company Name", "Tesla")

if st.sidebar.button("Fetch News"):
    st.sidebar.write("🔄 Fetching news articles from API...")

    # Call the API
    api_url = f"http://127.0.0.1:8000/get_news/{company_name}"
    response = requests.get(api_url)

    if response.status_code == 200:
        result = response.json()

        # Show comparative sentiment analysis
        st.subheader("📊 Comparative Sentiment Analysis")
        for insight in result["insights"]:
            st.write(insight)

        # Display news articles
        st.subheader("📰 Latest News Articles")
        for i, article in enumerate(result["articles"], 1):
            with st.expander(f"📢 Article {i}: {article['title']}"):
                st.write(f"🔗 [Read More]({article['link']})")
                st.write(f"📝 **Summary:** {article['summary']}")
                st.write(f"📊 **Sentiment:** {article['sentiment']}")
                st.audio(article["audio_file"])

    else:
        st.error("❌ Failed to fetch data from API.")
