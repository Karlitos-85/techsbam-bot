import os
import asyncio
import random
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# 🔐 Variabili ambientali
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")
TAG = os.getenv("AMAZON_TAG")

bot = Bot(token=TOKEN)

# 🎯 URL Amazon Offerte del Giorno
AMAZON_URL = "https://www.amazon.it/gp/goldbox"

# 🧠 Categorie da cercare
CATEGORIE = [
    "informatica", "tech", "gaming", "elettronica", "elettrodomestici",
    "smartwatch", "monitor", "tablet", "cuffie", "SSD", "stampante",
    "notebook", "tv 4k", "soundbar", "mouse", "tastiera", "router", "smart home"
]

# 📦 Funzione per estrarre offerte reali
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
            link = "https://www.amazon.it" + link_tag["href"]
            immagine = immagine_tag["src"]

            # ✅ Filtra solo link validi
            if ("/dp/" in link or "/gp/product/" in link) and "%" in sconto:
                valore = int(sconto.replace("%", "").replace("-", "").strip())
                if valore >= 8 and any(cat.lower() in titolo.lower() for cat in CATEGORIE):
                    offerte.append({
                        "titolo": titolo,
                        "prezzo": prezzo,
                        "sconto": sconto,
                        "link": f"{link}?tag={TAG}",
                        "immagine": immagine
                    })
    return offerte


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
            await bot.send_message(chat_id=CHANNEL, text="Oggi Amazon non ha voglia di sbam... riproviamo tra un'ora.")
        await asyncio.sleep(3600)  # ogni ora

if __name__ == "__main__":
    asyncio.run(main())
