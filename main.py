import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.constants import ParseMode

# ✅ Dati reali
TOKEN = "7968531317:AAFZuMH8XgWkMvSjE1Wof8Ujpm0-ffdizfc"
CHANNEL = "@techsbam"
TAG = "karlitos85-21"

# ✅ Scraping Amazon Offerte
def estrai_offerte():
    url = "https://www.amazon.it/gp/goldbox"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    offerte = []
    for div in soup.find_all("div", class_="DealContent"):
        titolo_tag = div.find("span", class_="DealTitle")
        prezzo_tag = div.find("span", class_="a-price-whole")
        link_tag = div.find("a")
        immagine_tag = div.find("img")

        if titolo_tag and prezzo_tag and link_tag:
            titolo = titolo_tag.get_text(strip=True)
            prezzo = prezzo_tag.get_text(strip=True)
            raw_link = link_tag["href"]
            immagine = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/1024px-Amazon_logo.svg.png"

            # Estrai ASIN
            asin = None
            if "/dp/" in raw_link:
                asin = raw_link.split("/dp/")[1].split("/")[0]
            elif "/gp/product/" in raw_link:
                asin = raw_link.split("/gp/product/")[1].split("/")[0]

            if asin:
                link = f"https://www.amazon.it/dp/{asin}/?tag={TAG}"
                offerte.append({
                    "titolo": titolo,
                    "prezzo": prezzo,
                    "link": link,
                    "immagine": immagine
                })

    return offerte

# ✅ Bot Telegram
async def main():
    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHANNEL,
        text="🛒 Tech & Sbam — offerte Amazon in arrivo!"
    )

    offerte = estrai_offerte()

    for prodotto in offerte:
        messaggio = (
            f"📦 *{prodotto['titolo']}*\n"
            f"💰 Prezzo: {prodotto['prezzo']}€\n"
            f"👉 [Vai all’offerta]({prodotto['link']})"
        )

        try:
            await bot.send_photo(
                chat_id=CHANNEL,
                photo=prodotto["immagine"],
                caption=messaggio,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(f"Errore nell'invio: {e}")

        await asyncio.sleep(3)

# ✅ Avvio
if __name__ == "__main__":
    asyncio.run(main())
