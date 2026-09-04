import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        errors = []
        page.on("console", lambda msg: errors.append(f"CONSOLE: {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda err: errors.append(f"PAGE ERROR: {err}"))
        
        await page.goto("http://localhost:3000/state-to-state-routes/california", wait_until="networkidle")
        await asyncio.sleep(2)
        
        if errors:
            print("ERRORS FOUND:")
            for e in errors:
                print(e)
        else:
            print("NO ERRORS FOUND.")
            
        await browser.close()

asyncio.run(run())
