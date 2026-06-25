import asyncio
import json
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_news():
    print("Agent is starting Script 1...")
    
    # Playwright start kar rahe hain
    async with async_playwright() as p:
        # Browser khol rahe hain (headless=False rakha hai taaki tu screen par magic dekh sake)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("Navigating to HackerNews...")
            # HackerNews website par ja rahe hain (timeout 15 seconds rakha hai as Error Handle #1)
            await page.goto("https://news.ycombinator.com/", timeout=15000)
            
            print("Website loaded! Looking for top 5 news titles...")
            # HackerNews par titles ki CSS class '.titleline' hoti hai (Error Handle #2 agar element na mile)
            await page.wait_for_selector(".titleline", timeout=5000)
            
            # Poore page ka HTML utha lo
            html_content = await page.content()
            
            # BeautifulSoup ko HTML de do taaki wo padh sake
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Saare titles dhoondho
            title_elements = soup.find_all('span', class_='titleline')
            
            # Pehle 5 titles ka text nikal kar list mein daalo
            top_5_titles = []
            for element in title_elements[:5]:
                top_5_titles.append(element.text.strip())
            
            # Unko outputs folder mein JSON file banakar save kar do
            with open("outputs/news_titles.json", "w") as f:
                json.dump(top_5_titles, f, indent=4)
                
            print("\nSUCCESS! Top 5 titles nikal kar 'outputs/news_titles.json' mein save ho gaye hain.")

        except Exception as e:
            # Agar net band ho ya website down ho toh yeh error aayegi
            print(f"Bhai koi error aa gayi: {e}")
            
        finally:
            # Kaam khatam hone ke baad browser zaroor band karna hai
            await asyncio.sleep(2) # 2 second wait kar raha hu taaki tu browser dekh sake
            await browser.close()
            print("Script 1 complete!\n")

# Yahan se program chalna shuru hota hai
if __name__ == "__main__":
    asyncio.run(scrape_news())