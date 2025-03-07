import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send /meme for fresh memes!")

async def send_meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        meme = requests.get("https://meme-api.com/gimme").json()
        if not meme["nsfw"]:
            await update.message.reply_photo(
                photo=meme["url"],
                caption=f"😂 {meme['title']} (r/{meme['subreddit']})"
            )
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

if __name__ == "__main__":
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("meme", send_meme))
    application.run_polling()
