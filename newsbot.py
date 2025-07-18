import asyncio
import feedparser
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError
import time

# === CONFIG ===
BOT_TOKEN = "8043966461:AAF_G44YIVHvG3i3sBGP4nuQdx9egRhRhAU"
CHANNEL_ID = "@freeearningstetantes"  # channel username or ID
FEED_URLS = [
    "https://cointelegraph.com/rss",  # Replace or add more RSS URLs here
]
POST_INTERVAL = 180  # seconds between post checks
TAG = "@freeearningstetantes"  # Optional tag in each post

# Cache for posted links
posted_links = set()

bot = Bot(token=BOT_TOKEN)

async def fetch_and_post_news():
    print("🔁 Checking feeds...")
    for url in FEED_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # limit per run
            link = entry.link
            title = entry.title
            summary = entry.get("summary", "")

            if link in posted_links:
                continue  # skip already posted

            message = f"<b>{title}</b>\n\n{TAG}\n<a href='{link}'>Read more</a>"

            try:
                await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=message,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=False
                )
                print(f"✅ Posted: {title}")
                posted_links.add(link)
            except TelegramError as e:
                print(f"❌ Failed to send: {e}")
            await asyncio.sleep(2)  # short pause between messages to avoid flood

async def main():
    print("🤖 Starting Crypto News Bot...")
    while True:
        await fetch_and_post_news()
        print(f"⏳ Waiting {POST_INTERVAL} seconds...\n")
        await asyncio.sleep(POST_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())