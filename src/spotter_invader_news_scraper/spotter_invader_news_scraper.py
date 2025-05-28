import json
import re
import requests
from bs4 import BeautifulSoup
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional

# Configure logging (set level to DEBUG)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


EMOJI_MAP = {"dg": "💥⬇️", "ko": "💀❌", "ok": "✅✨", "nt": "ℹ️🔄", "wn": "⚠️📢"}
KEYWORD_MAP = {
    "dg": "Degraded",
    "ko": "Destroyed",
    "ok": "Created",
    "nt": "Updated",
    "wn": "Alert",
}


@dataclass
class MosaicUpdate:
    mosaic_id: str
    action_type: str

    def __str__(self) -> str:
        """Returns a concise string representation of the MosaicUpdate."""
        emoji = EMOJI_MAP.get(self.action_type, "❓")  # Default emoji if unknown
        keyword = KEYWORD_MAP.get(
            self.action_type, self.action_type
        )  # Default to action_type if unknown
        return f"{emoji} {keyword}: {self.mosaic_id}"


@dataclass
class DailyNews:
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
    updates: List[MosaicUpdate]

    def group_updates_by_action_type(self) -> Dict[str, List[str]]:
        """Groups the mosaic updates by their action type.

        Returns:
            Dict[str, List[str]]: A dictionary where keys are action types
                                 and values are lists of mosaic IDs.
        """
        grouped_updates: Dict[str, List[str]] = {}
        for update in self.updates:
            if update.action_type not in grouped_updates:
                grouped_updates[update.action_type] = []
            grouped_updates[update.action_type].append(update.mosaic_id)
        return grouped_updates

    def __str__(self) -> str:
        """Returns a concise string representation of the DailyNews."""

        if not self.updates:
            return f"🗓️ {self.year}-{self.month:02d}-{self.day:02d}: No updates"

        return (
            f"🗓️ {self.year}-{self.month:02d}-{self.day:02d}: \n\n"
            + "\n".join(
                [
                    f'{EMOJI_MAP.get(action_type, "❓")}  {KEYWORD_MAP.get(action_type, action_type):10s}: {", ".join(mosaic_ids)}'
                    for action_type, mosaic_ids in self.group_updates_by_action_type().items()
                ]
            )
            + "\n"
        )


@dataclass
class MonthlyNews:
    year: Optional[int]
    month: Optional[int]
    news_blocks: List[str]


def extract_news_blocks(html_content: str, year: int, month: int) -> MonthlyNews:
    soup = BeautifulSoup(html_content, "html.parser")
    month_str = f"{year}{month:02d}"  # e.g. 202505
    news_div = soup.find("div", id=f"mois{month_str}")
    regex = re.compile(
        r'<p class="news"><b>\d+ :</b>.*?(?=<p class="news"><b>\d+ :</b>|\Z)', re.DOTALL
    )
    news_blocks = regex.findall(news_div.decode_contents())
    return MonthlyNews(news_blocks=news_blocks, year=year, month=month)


def extract_news_info(news_block: str, year: int, month: int) -> Optional[DailyNews]:
    try:
        soup = BeautifulSoup(news_block, "html.parser")

        # Extract the day
        day_tag = soup.find("b")
        day: Optional[int] = int(day_tag.text.replace(" :", "")) if day_tag else None

        # Extract updates
        updates: List[MosaicUpdate] = []
        for a_tag in soup.find_all("a"):
            mosaic_id = a_tag.text.strip()
            action_type = a_tag.get("class")[0] if a_tag.get("class") else "unknown"
            updates.append(MosaicUpdate(mosaic_id=mosaic_id, action_type=action_type))

        return DailyNews(day=day, updates=updates, year=year, month=month)

    except Exception as e:
        logging.error(f"Error extracting news info: {e}")
        return None
