from .. import spotter_invader_news_scraper as scraper
import requests


def test_get_monthly_news():
    url = "https://www.invader-spotter.art/news.php"
    response = requests.get(url)
    year = 2025
    month = 3

    monthly_news: scraper.MonthlyNews = scraper.extract_news_blocks(
        response.content, year, month
    )

    for news_block in monthly_news.news_blocks:
        daily_news = scraper.extract_news_info(news_block, year, month)
        if daily_news:
            print(daily_news)
    assert len(monthly_news.news_blocks) == 24
