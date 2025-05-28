import telegram
from telegram.helpers import escape_markdown
import asyncio
import logging
from config.config import TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def send_message(message):
    bot = telegram.Bot(TELEGRAM_BOT_TOKEN)
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=escape_markdown(message, 2, telegram.constants.ParseMode.MARKDOWN_V2),
            parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
        )
        logging.info(f"Message sent to chat ID {TELEGRAM_CHAT_ID} with MarkdownV2")
    except telegram.error.TelegramError as e:
        logging.error(f"Error sending message to chat ID {TELEGRAM_CHAT_ID}: {e}")


async def main():
    await send_message("This is a *test* with **bold**.")


if __name__ == "__main__":
    asyncio.run(main())
