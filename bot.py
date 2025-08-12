import asyncio
from playwright.async_api import async_playwright
import requests
import time
from bs4 import BeautifulSoup

WEBHOOK_URL = https://discord.com/api/webhooks/1404934186313318593/Dg1K8XWa0UiT4nfoloJ9A4iHfIctTTpv7FDWOMjw885_KtRTAvrm4Ssn7aegLd1cgda4
URL_MARKETPLACE = https://www.facebook.com/marketplace/oslo/cars?maxPrice=120000&exact=false
CHECK_INTERVAL = 300  # 5 minut

seen_ads = set()

async def get_ads():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL_MARKETPLACE, timeout=60000)
        await page.wait_for_timeout(5000)
        html = await page.content()
        await browser.close()

        soup = BeautifulSoup(html, "html.parser")
        ads = []
        for ad in soup.find_all("a", href=True):
            if "/marketplace/item/" in ad["href"]:
                link = "https://facebook.com" + ad["href"].split("?")[0]
                title = ad.get_text(strip=True)
                ads.append((title, link))
        return ads

async def main():
    global seen_ads
    while True:
        try:
            ads = await get_ads()
            for title, link in ads:
                if link not in seen_ads:
                    seen_ads.add(link)
                    requests.post(WEBHOOK_URL, json={"content": f"📢 Nowe ogłoszenie: {title}\n{link}"})
        except Exception as e:
            print("Błąd:", e)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
Add bot.py
