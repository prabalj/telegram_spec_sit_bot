import requests
from bs4 import BeautifulSoup
import datetime
import os

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

NEWS_SOURCES = [
    "https://www.moneycontrol.com/news/business/deals/",
    "https://economictimes.indiatimes.com/markets/deals",
  "https://www.bseindia.com/corporates/ann.html",
  "https://www.nseindia.com/companies-listing/corporate-filings-announcements"
]

def get_headlines():
    headlines = []
    try:
        mc_resp = requests.get(NEWS_SOURCES[0])
        soup = BeautifulSoup(mc_resp.content, 'html.parser')
        for link in soup.select('li.clearfix a'):
            title = link.get_text(strip=True)
            url = link['href']
            if any(k in title.lower() for k in ['merger', 'acquisition', 'buyback','open offer', 'ashish kacholia', 'preferential allotment', 'mukul agarwal', 'stake', 'demerger']):
                headlines.append(f"📰 {title}\n🔗 {url}")
    except Exception as e:
        headlines.append(f"Moneycontrol error: {e}")

    try:
        et_resp = requests.get(NEWS_SOURCES[1])
        soup = BeautifulSoup(et_resp.content, 'html.parser')
        for item in soup.select('div.eachStory'):
            title_tag = item.select_one('h3 a')
            if title_tag:
                title = title_tag.get_text(strip=True)
                url = "https://economictimes.indiatimes.com" + title_tag['href']
                if any(k in title.lower() for k in ['merger', 'acquisition', 'open offer', 'stake', 'demerger']):
                    headlines.append(f"📰 {title}\n🔗 {url}")
    except Exception as e:
        headlines.append(f"ET error: {e}")

    return headlines

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def run_bot():
    headlines = get_headlines()
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    if not headlines:
        send_telegram_message(f"No M&A or special situation news found on {date_str}.")
    else:
        send_telegram_message(f"*🧾 M&A News for {date_str}:*\n\n" + "\n\n".join(headlines))

if __name__ == "__main__":
    run_bot()
