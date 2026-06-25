import asyncio
from playwright.async_api import async_playwright

async def manage_multiple_tabs():
    print("Agent is starting Script 3: Tab Manager (Parallel Mode)...")
    
    # Hum 5 alag-alag websites ki list bana rahe hain
    urls = [
        "https://www.example.com",
        "https://news.ycombinator.com",
        "https://www.wikipedia.org",
        "https://github.com",
        "https://www.python.org"
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        # Naya 'context' bana rahe hain. 
        # Context ek incognito window jaisa hota hai jiske andar saare tabs khulenge.
        context = await browser.new_context()
        
        try:
            # 1. 5 khali tabs (pages) create karte hain
            pages = []
            for _ in range(5):
                pages.append(await context.new_page())
                
            print("5 empty tabs created. Loading websites in PARALLEL...")

            # Yeh function ek single tab mein website load karega aur title nikalega
            async def load_and_get_title(page, url, tab_number):
                try:
                    # Timeout error handling (Error condition 1)
                    await page.goto(url, timeout=15000)
                    title = await page.title()
                    print(f"Tab {tab_number} Loaded: {title}")
                except Exception as e:
                    print(f"Tab {tab_number} failed to load {url}. Error: {e}")

            # 2. asyncio.gather se hum paancho tabs ko ek saath (parallel) kaam pe laga rahe hain
            tasks = []
            for i in range(5):
                # Har page ko uska url aur tab number de rahe hain
                tasks.append(load_and_get_title(pages[i], urls[i], i+1))
                
            # Boom! Saare tasks ek sath run honge
            await asyncio.gather(*tasks)
            
            print("\nSaari websites load ho gayi! 3 second ruko...")
            await asyncio.sleep(3)
            
            # 3. Pehle tab (index 0) ko chhod kar baaki 4 tabs (index 1 to 4) close kar rahe hain
            print("Closing tabs 2, 3, 4, and 5...")
            for i in range(1, 5):
                await pages[i].close()
                print(f"Closed Tab {i+1}")
            
            print("\nMISSION ACCOMPLISHED: Only the first tab is open.")
            
        except Exception as e:
            # Overall system error handling (Error condition 2)
            print(f"System Error in Tab Manager: {e}")
            
        finally:
            # Aakhri tab dekhne ke liye 2 second ka pause, phir browser band
            await asyncio.sleep(2)
            await browser.close()
            print("Script 3 complete!\n")

# Yahan se program chalna shuru hota hai
if __name__ == "__main__":
    asyncio.run(manage_multiple_tabs())