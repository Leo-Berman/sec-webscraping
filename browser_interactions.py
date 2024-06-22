import asyncio
import pyppeteer as pt

async def initialize_browser(link):
    browser = await pt.launch({"headless" : False})
    page = await browser.newPage()

    await page.goto(link,{"waitUntil" : ['domcontentloaded',
                    'networkidle2','networkidle0'] })

    return page

async def find_table(page):