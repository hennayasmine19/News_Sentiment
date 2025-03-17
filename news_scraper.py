from gnews import GNews
from sentiment_analysis import analyze_sentiment
from text_to_speech import text_to_speech
from collections import Counter

def fetch_news(company_name, num_articles=10):
    """
    Fetches news articles, performs sentiment analysis, and generates comparative insights.

    Args:
        company_name (str): The company to search for.
        num_articles (int): Number of news articles to extract.

    Returns:
        dict: Contains articles, sentiment distribution, and comparative insights.
    """
    google_news = GNews(language="hi", country="IN", max_results=num_articles)
    news_list = google_news.get_news(company_name)

    articles = []
    sentiments = []
    
    for i, news in enumerate(news_list, start=1):
        summary = news["description"]
        sentiment = analyze_sentiment(summary)
        sentiments.append(sentiment)  # Store sentiments for comparative analysis
        
        # Convert summary to Hindi speech
        audio_filename = text_to_speech(summary, f"{company_name}_news_{i}.mp3")

        articles.append({
            "title": news["title"],
            "link": news["url"],
            "summary": summary,
            "sentiment": sentiment,
            "audio_file": audio_filename
        })

    # **Comparative Sentiment Analysis**
    sentiment_distribution = Counter(sentiments)

    # **Generate Insights**
    insights = []
    total_articles = sum(sentiment_distribution.values())

    insights.append(f"📊 Sentiment Distribution in {total_articles} articles:")
    insights.append(f"✅ {sentiment_distribution['Positive']} Positive")
    insights.append(f"⚠️ {sentiment_distribution['Negative']} Negative")
    insights.append(f"ℹ️ {sentiment_distribution['Neutral']} Neutral")

    # Determine overall sentiment trend
    if sentiment_distribution['Positive'] > sentiment_distribution['Negative']:
        insights.append("🟢 The majority of news articles are positive, suggesting a favorable outlook.")
    elif sentiment_distribution['Negative'] > sentiment_distribution['Positive']:
        insights.append("🔴 The majority of news articles are negative, indicating concerns about the company.")
    else:
        insights.append("🟡 There is a balanced mix of positive and negative coverage.")

    return {
        "articles": articles,
        "sentiment_distribution": dict(sentiment_distribution),
        "insights": insights
    }

# Example Usage
if __name__ == "__main__":
    company = input("Enter company name: ")
    result = fetch_news(company)

    if result["articles"]:
        print("\n" + "=" * 50)
        for i, article in enumerate(result["articles"], 1):
            print(f"\n📢 Article {i}:")
            print(f"📰 Title: {article['title']}")
            print(f"🔗 Link: {article['link']}")
            print(f"📝 Summary: {article['summary']}")
            print(f"📊 Sentiment: {article['sentiment']}")
            print(f"🔊 Audio File: {article['audio_file']} (Hindi Speech Generated)")

        print("\n📈 Comparative Sentiment Analysis:")
        for insight in result["insights"]:
            print(insight)
    else:
        print("❌ No articles found.")
