from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

signs = {
    "aries": "belier", "taurus": "taureau", "gemini": "gemeaux",
    "cancer": "cancer", "leo": "lion", "virgo": "vierge",
    "libra": "balance", "scorpio": "scorpion", "sagittarius": "sagittaire",
    "capricorn": "capricorne", "aquarius": "verseau", "pisces": "poissons"
}

def scrape_mon_horoscope(sign):
    url = f"https://www.mon-horoscope-du-jour.com/horoscopes/quotidien/{sign}.htm"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    horoscope = soup.find("p", class_="txt_avenir")
    return horoscope.text.strip() if horoscope else ""

def scrape_20minutes(sign):
    url = f"https://www.20minutes.fr/horoscope/{sign}"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    horoscope = soup.find("div", class_="horo-content")
    return horoscope.text.strip() if horoscope else ""

def reformulate(h1, h2):
    phrases = (h1 + " " + h2).split(". ")
    random.shuffle(phrases)
    return ". ".join(phrases).strip() + "."

@app.route('/horoscope', methods=['GET'])
def horoscope():
    result = {}
    for signe, nom in signs.items():
        h1 = scrape_mon_horoscope(nom)
        h2 = scrape_20minutes(nom)
        texte = reformulate(h1, h2) if h1 and h2 else "Horoscope indisponible"
        result[signe] = texte
    return jsonify(result)

if __name__ == '__main__':
    app.run()
