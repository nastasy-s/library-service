import os
import asyncio
import telegram


def send_telegram_message(message: str) -> None:
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Telegram credentials not set")
        return

    async def send():
        bot = telegram.Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message)

    asyncio.run(send())
