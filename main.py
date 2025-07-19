import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.constants import ParseMode

# ✅ Dati reali
TOKEN = "7968531317:AAFZuMH8XgWkMvSjE1Wof8Ujpm0-ffdizfc"
CHANNEL = "@techsbam"
TAG = "karlitos85-21"

AMAZON_URL = "https://www.amazon.it/gp/goldbox"
CATEGORIE = [
    "ssd", "hard disk", "monitor", "mouse", "tastiera", "auricolare",
    "cuffie", "usb", "router", "smartwatch", "raspberry", "tech",
    "tv", "android", "notebook", "tablet"
]

# ✅ Funzione aggiornata: estrai offerte reali da Amazon
def estrai_offerte():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(AMAZON_URL, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    offerte = []
    for div in soup.find_all("div", class_="DealContent"):
        titolo_tag = div.find("span", class_="DealTitle")
        prezzo_tag = div.find("span", class_="a-price-whole")
        sconto_tag = div.find("span", class_="a-size-mini")
        link_tag = div.find("a")
        immagine_tag = div.find("img")

        if titolo_tag and prezzo_tag and sconto_tag and link_tag and immagine_tag:
            titolo = titolo_tag.get_text(strip=True)
            prezzo = prezzo_tag.get_text(strip=True)
            sconto = sconto_tag.get_text(strip=True)
            raw_link = link_tag["href"]
            immagine = immagine_tag["src"]

            # Estrai l'ASIN dal link
            asin = None
            if "/dp/" in raw_link:
                asin = raw_link.split("/dp/")[1].split("/")[0]
            elif "/gp/product/" in raw_link:
                asin = raw_link.split("/gp/product/")[1].split("/")[0]

            # Costruisci link valido solo se c'è l'ASIN
            if asin and "%" in sconto:
                valore = int(sconto.replace("%", "").replace("-", "").strip())
                if valore >= 8 and any(cat.lower() in titolo.lower() for cat in CATEGORIE):
                    link = f"https://www.amazon.it/dp/{asin}/?tag={TAG}"
                    offerte.append({
                        "titolo": titolo,
                        "prezzo": prezzo,
                        "sconto": sconto,
                        "link": link,
                        "immagine": immagine
                    })

    return offerte

# ✅ Funzione principale del bot
async def main():
    bot = Bot(token=TOKEN)

    # Messaggio di benvenuto
    await bot.send_message(
        chat_id=CHANNEL,
        text="Benvenuti su Tech & Sbam 💥 — le offerte Amazon arrivano puntuali come il caffè!"
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

        await asyncio.sleep(3)  # 🕒 Pausa per evitare flood Telegram

# ✅ Avvio del bot
if __name__ == "__main__":
    asyncio.run(main())
