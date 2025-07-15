import requests
import time
import os
from telegram import Bot

# إعدادات
RSI_API_URL = "https://finnhub.io/api/v1/indicator?symbol=EURUSD&resolution=5&indicator=rsi&timeperiod=14&token=" + os.getenv("FINNHUB_API_KEY")
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# بوت التليجرام
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")

def get_rsi():
    try:
        response = requests.get(RSI_API_URL)
        data = response.json()
        if 'rsi' in data and data['rsi']:
            return data['rsi'][-1]
    except Exception as e:
        print("Error getting RSI:", e)
    return None

def main():
    print("Bot is running...")
    last_alert = ""
    while True:
        rsi = get_rsi()
        if rsi is not None:
            print("RSI:", rsi)
            if rsi < RSI_OVERSOLD and last_alert != "low":
                bot.send_message(chat_id=chat_id, text=f"🔻 RSI منخفض: {rsi:.2f} (أقل من 30)")
                last_alert = "low"
            elif rsi > RSI_OVERBOUGHT and last_alert != "high":
                bot.send_message(chat_id=chat_id, text=f"🔺 RSI مرتفع: {rsi:.2f} (أعلى من 70)")
                last_alert = "high"
        time.sleep(60)

if __name__ == "__main__":
    main()