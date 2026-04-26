import asyncio
from patchright.async_api import async_playwright
import json

PHANTOM_DIR = "PATH_TO_YOUR_PHANTOM_EXTENSION"
WORKDIR = "PATH_TO_YOUR_PROFILE"
TOKEN_NAME = "YOUR_TOKEN_NAME"
TOKEN_SYMBOL = "YOUR_TOKEN_NAME"
TOKEN_DESCRIPTION = "YOUR_TOKEN_DESCRIPTION"
AMOUNT = "0.01"
PHANTOM_PASSWORD = "YOUR_PHANTOM_PASS"
IMAGE_PATH = "PATH_TO_YOUR_IMAGE"

async def launch():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=WORKDIR,
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                f'--disable-extensions-except={PHANTOM_DIR}',
                f'--load-extension={PHANTOM_DIR}',
            ],
        )
        with open("PATH_TO_YOUR_COOKIES/cookies.json", "r") as f:
            cookies = json.loads(f.read())
            await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto('https://pump.fun/create')
        print("Token creation form opened")
        await asyncio.sleep(3)

        ready = page.locator("[data-test-id='how-it-works-button']")
        if await ready.is_visible():
            await ready.click()
            await asyncio.sleep(1)

        name = page.get_by_role("textbox", name="name")
        if await name.is_visible():
            await name.fill(TOKEN_NAME)
            await asyncio.sleep(1)

        ticker = page.locator("[id='ticker']")
        if await ticker.is_visible():
            await ticker.fill(TOKEN_SYMBOL)
            await asyncio.sleep(1)

        desc = page.locator("[id='text']")
        if await desc.is_visible():
            await desc.fill(TOKEN_DESCRIPTION)
            await asyncio.sleep(1)

        cashback = page.locator('[role="switch"]').last
        if await cashback.is_visible():
            await cashback.click()
            print("Cashback enabled!")
        await asyncio.sleep(1)        
        file_input = page.locator('input[type="file"]')
        await file_input.wait_for(state="attached")
        await file_input.set_input_files(IMAGE_PATH)
        print("Photo uploaded!")
        await asyncio.sleep(2)

        creates = page.get_by_role('button', name="Create coin")
        for i in range(await creates.count()):
            btn = creates.nth(i)
            if await btn.is_visible() and await btn.is_enabled():
                await btn.click()
                print("Clicked first Create coin!")
                await asyncio.sleep(3)
                break

        amount = page.locator("[id='amount']")
        if await amount.is_visible():
            await amount.fill(AMOUNT)
            print("Amount entered!")
            await asyncio.sleep(4)

        await page.evaluate("""
            const buttons = Array.from(document.querySelectorAll('button'));
            const last = buttons.filter(b => b.innerText.trim() === 'Create coin').pop();
            if (last) last.click();
        """)
        print("Clicked second Create coin!")
        await asyncio.sleep(6)

        for phantom in context.pages:
            if 'notification.html' in phantom.url:
                print("Phantom found!")
                await phantom.bring_to_front()
                await asyncio.sleep(2)
                await asyncio.sleep(2)
                await phantom.locator('input[type="password"]').fill(PHANTOM_PASSWORD)
                await phantom.locator('input[type="password"]').press('Enter')
                print("Password entered!")
                await asyncio.sleep(3)
                confirm = phantom.get_by_test_id('primary-button')
                if await confirm.is_visible():
                    await confirm.click()
                    print("Phantom confirmed!")

        print("Done!")
        await asyncio.sleep(15)
        await context.close()

asyncio.run(launch())
