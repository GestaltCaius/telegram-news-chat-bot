import asyncio
from typing import List
import requests
from src.telegram_bot.telegram_bot import send_message
from src.spotter_invader_news_scraper.spotter_invader_news_scraper import (
    extract_news_blocks,
    extract_news_info,
    MonthlyNews,
    DailyNews,
)
from datetime import datetime
import logging
import argparse
import re

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def main(year, month, day):
    url = "https://www.invader-spotter.art/news.php"
    search_day = day
    search_month = month
    search_year = year

    response = requests.get(url)

    # Get all month news
    monthly_news: MonthlyNews = extract_news_blocks(
        response.content, year, month
    )  # Changed function call

    # Parse all month news
    daily_news: List[DailyNews] = [
        extract_news_info(news_block, year, month)
        for news_block in monthly_news.news_blocks
    ]
    queried_news = next((n for n in daily_news if n.day == day), None)

    if queried_news:
        await send_message(str(queried_news))
        logging.info(f"sending msg :{str(queried_news)}")
    else:
        logging.info(
            f"No updates to send for {search_day}/{search_month}/{search_year}."
        )


if __name__ == "__main__":
    today = datetime.now()
    parser = argparse.ArgumentParser(
        description="Scrape Invader Spotter news and send to Telegram."
    )
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        default=today.year,
        help="The year to fetch news for (default: current year).",
    )
    parser.add_argument(
        "-m",
        "--month",
        type=int,
        default=today.month,
        help="The month to fetch news for (default: current month).",
    )
    parser.add_argument(
        "-d",
        "--day",
        type=int,
        default=today.day,
        help="The day to fetch news for (default: current day).",
    )
    args = parser.parse_args()

    asyncio.run(main(year=args.year, month=args.month, day=args.day))
