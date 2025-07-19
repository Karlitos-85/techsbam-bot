import asyncio
import requests
from telegram import Bot
from telegram.constants import ParseMode

# ✅ Dati reali
TOKEN = "6110414793:AAE6USmIOGUOGWAnwEX9UxtTxmbMZot1jYY"
CHANNEL = "@techsbam"
TAG = "karlitos85-21"

# ✅ Offerta di test
def estrai_offerte():
    return [{
        "titolo": "SSD Samsung 980 1TB NVMe",
        "prezzo": "69,99€",
        "sconto": "22%",
        "link": f"https://www.amazon.it/dp/B08N5M7S6K/?tag={TAG}",
        "immagine": "https://m.media-amazon.com/images/I/61EQdeD3lXL._AC_SL1500_.jpg"
    }]

# ✅ Funzione principale
async def main():
    bot = Bot(token=TOKEN)

    # Messaggio di benvenuto
    await bot.send_message(
        chat_id=CHANNEL,
        text="Benvenuti su Tech & Sbam 💥 — dove le offerte Amazon sono più puntuali di me alla pausa pranzo."
    )

    offerte = estrai_offerte()

    for prodotto in offerte:
        messaggio = (
            f"📦 {prodotto['titolo']}\n"
            f"💰 Prezzo: {prodotto['prezzo']}\n"
            f"🔻 Sconto: {prodotto['sconto']}\n"
            f"👉 [Vai all’offerta]({prodotto['link']})"
        )

        # 🕒 Pausa per evitare flood Telegram
        await asyncio.sleep(2)

        # Invio immagine + caption
        await bot.send_photo(
            chat_id=CHANNEL,
            photo=prodotto["immagine"],
            caption=messaggio,
            parse_mode=ParseMode.MARKDOWN
        )

# ✅ Avvio bot
if __name__ == "__main__":
    asyncio.run(main())

# 🧠 Frasi ironiche
intro = [
    "📦 Amazon ci vizia oggi... come se avesse sensi di colpa.",
    "🎮 Sconto tech o provocazione personale? Decidi tu.",
    "⚠️ Offerta che non puoi ignorare (ma puoi far finta di sì)",
    "🥲 Hai detto 'non spendo più'? Mi dispiace.",
    "🔌 Offerta tech — ma solo se lo meriti. Tu lo meriti."
]

# 🚀 Funzione principale
async def main():
    await bot.send_message(chat_id=CHANNEL, text="Benvenuti su Tech & Sbam 💥 — dove le offerte Amazon sono più puntuali di me alla pausa pranzo.")
    while True:
        offerte = estrai_offerte()
        if offerte:
            prodotto = random.choice(offerte)
            messaggio = f"{random.choice(intro)}\n\n🛒 {prodotto['titolo']}\n💸 Prezzo: {prodotto['prezzo']} (-{prodotto['sconto']})\n➡️ {prodotto['link']}\n\n#TechSbamDelGiorno"
            await bot.send_photo(chat_id=CHANNEL, photo=prodotto["immagine"], caption=messaggio)
        else:
           await bot.send_message(chat_id=CHANNEL, text=messaggio)
await asyncio.sleep(3)  # evita flood
await bot.send_photo(chat_id=CHANNEL, photo=prodotto["immagine"])

if __name__ == "__main__":
    asyncio.run(main())
