import streamlit as st
from news_scraper import fetch_news

# Streamlit App UI
st.set_page_config(page_title="News Sentiment Analysis", layout="wide")

st.title("📰 News Sentiment Analysis & Hindi Text-to-Speech")

# User input
st.sidebar.header("Enter a Company Name")
company_name = st.sidebar.text_input("Company Name", "Tesla")

if st.sidebar.button("Fetch News"):
    st.sidebar.write("🔄 Fetching news articles...")

    # Call fetch_news() directly (No API needed)
    result = fetch_news(company_name)

    if result["articles"]:
        st.sidebar.success(f"✅ Found {len(result['articles'])} articles!")

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
        st.error("❌ No articles found. Try another company.")
