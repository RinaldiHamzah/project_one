import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
import requests

BOT_TOKEN = "8128015859:AAHy4JWf-4G4zssuaKKwWCbAOkKC3h9M65o"

# === Handler untuk /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"Chat ID kamu: {chat_id}")
    await update.message.reply_text("Hai! Kirimkan review, saya akan analisis sentimennya.")

# === Handler untuk pesan teks biasa ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    prediction = "POSITIF"  # placeholder
    print(f"Pesan diterima dari {update.effective_user.first_name}: {text}")
    await update.message.reply_text(f"Prediksi sentimen: {prediction}")

# === Jalankan bot ===
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # tambahkan handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot Telegram aktif...")

    # --- penting: inisialisasi async manual ---
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()   # biar event loop tetap jalan

if __name__ == "__main__":
    asyncio.run(main())
