import asyncio
from telegram import Bot
from telegram.constants import ParseMode

# ✅ Dati reali
TOKEN = "6110414793:AAE6USmIOGUOGWAnwEX9UxtTxmbMZot1jYY"
CHANNEL = "@techsbam"
TAG = "karlitos85-21"

# ✅ Offerta di test (solo testo, niente immagine)
def estrai_offerte():
    return [{
        "titolo": "SSD Samsung 980 1TB NVMe",
        "prezzo": "69,99€",
        "sconto": "22%",
        "link": f"https://www.amazon.it/dp/B08N5M7S6K/?tag={TAG}"
    }]

# ✅ Funzione principale
async def main():
    bot = Bot(token=TOKEN)

    # Messaggio di benvenuto
    await bot.send_message(
        chat_id=CHANNEL,
        text="Benvenuti su Tech & Sbam 💥 — dove le offerte Amazon arrivano puntuali come il caffè!"
    )

    offerte = estrai_offerte()

    for prodotto in offerte:
        messaggio = (
            f"📦 *{prodotto['titolo']}*\n"
            f"💰 Prezzo: {prodotto['prezzo']}\n"
            f"🔻 Sconto: {prodotto['sconto']}\n"
            f"👉 [Vai all’offerta]({prodotto['link']})"
        )

        try:
            await bot.send_message(
                chat_id=CHANNEL,
                text=messaggio,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(f"Errore nell'invio: {e}")

        await asyncio.sleep(3)  # Pausa per evitare flood

# ✅ Avvio bot
if __name__ == "__main__":
    asyncio.run(main())
