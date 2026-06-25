import asyncio
import json
from playwright.async_api import async_playwright

async def fill_demoqa_form():
    print("Agent is starting Script 2: Form Filler...")
    
    # 1. JSON file se data padhna
    try:
        with open("inputs/form_data.json", "r") as f:
            user_data = json.load(f)
    except Exception as e:
        print("Bhai inputs folder aur form_data.json check kar! Error:", e)
        return

    # Playwright start kar rahe hain
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("DemoQA form par jaa rahe hain...")
            # Timeout error handling (Error condition 1)
            await page.goto("https://demoqa.com/automation-practice-form", timeout=20000)
            
            print("Website load ho gayi! Ab automatically form bharte hain...")
            
            # 2. Form fill karna (.fill function aur CSS selectors ka use)
            # Timeout=5000 isliye lagaya taaki agar input box na mile toh error handle ho jaye (Error condition 2)
            await page.fill("#firstName", user_data["firstName"], timeout=5000)
            await page.fill("#lastName", user_data["lastName"])
            await page.fill("#userEmail", user_data["userEmail"])
            
            # DemoQA par gender select karna zaroori hai varna form aage nahi badhta (Radio button)
            await page.click("label[for='gender-radio-1']") 
            
            await page.fill("#userNumber", user_data["userNumber"])
            await page.fill("#currentAddress", user_data["currentAddress"])
            
            print("Form bhar diya! Ab screenshot le rahe hain...")
            
            # 3. Screenshot lena aur outputs folder mein save karna
            await page.screenshot(path="outputs/form_proof.png", full_page=True)
            print("SUCCESS! Screenshot 'outputs/form_proof.png' mein save ho gaya hai.")

        except Exception as e:
            # Agar koi element nahi mila ya net gaya toh crash nahi hoga
            print(f"Error aa gayi form bharte waqt: {e}")
            
        finally:
            # Thoda wait karke browser band (taaki tu bhara hua form dekh sake)
            await asyncio.sleep(2)
            await browser.close()
            print("Script 2 complete!\n")

# Yahan se code run hoga
if __name__ == "__main__":
    asyncio.run(fill_demoqa_form())