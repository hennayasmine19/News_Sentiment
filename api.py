from fastapi import FastAPI
from news_scraper import fetch_news

app = FastAPI()

@app.get("/get_news/{company_name}")
def get_news(company_name: str):
    """
    Fetches news articles, performs sentiment analysis, and returns results via API.

    Args:
        company_name (str): The company to search for.

    Returns:
        dict: News articles with sentiment analysis.
    """
    result = fetch_news(company_name)
    return result

# Run the API using: uvicorn api:app --reload
