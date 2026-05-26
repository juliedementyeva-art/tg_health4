
# bot.py
# Упрощённый запуск Telegram-бота
# pip install python-telegram-bot==21.6 pandas matplotlib openpyxl python-dotenv

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import time
import os

BOT_TOKEN=os.getenv("BOT_TOKEN")

METRICS=["Физическое здоровье","Эмоциональное здоровье","Интеллектуальное здоровье","Духовное здоровье"]

def keyboard(metric_index):
    rows=[]
    row=[]
    for i in range(1,11):
        row.append(InlineKeyboardButton(str(i), callback_data=f"{metric_index}:{i}"))
        if len(row)==5:
            rows.append(row)
            row=[]
    return InlineKeyboardMarkup(rows)

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет 🌿 Нажми /checkin"
    )

async def checkin(update:Update, context:ContextTypes.DEFAULT_TYPE):
    context.user_data["i"]=0
    await update.message.reply_text(
        f"{METRICS[0]} (1–10)",
        reply_markup=keyboard(0)
    )

async def click(update:Update, context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    await q.answer()

    metric_i,val=q.data.split(":")
    metric_i=int(metric_i)

    await q.edit_message_text(f"✅ {METRICS[metric_i]}: {val}")

    next_i=metric_i+1
    if next_i<len(METRICS):
        await q.message.reply_text(
            f"{METRICS[next_i]} (1–10)",
            reply_markup=keyboard(next_i)
        )
    else:
        await q.message.reply_text("Готово 🎉")

import asyncio

app=Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("checkin",checkin))
app.add_handler(CallbackQueryHandler(click))

print("bot started")

async def main():
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)

asyncio.run(main())
