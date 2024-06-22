import asyncio
import pyppeteer as pt
import unicodedata
import pandas as pd
import pdb

import process_table as ptab

async def initialize_browser(link):
    browser = await pt.launch({"headless" : False})
    page = await browser.newPage()

    await page.goto(link,{"waitUntil" : ['domcontentloaded',
                    'networkidle2','networkidle0'] })

    return page,browser

async def find_frame(page):

    for frame in page.frames:
        if frame.name == "ixvFrame":
            return frame

async def narrow_divs(divs,date):

    for index,div in enumerate(divs):
        content = await div.getProperty("textContent")
        text = unicodedata.normalize('NFKC',content.toString()).replace("JSHandle:","")

        if text.__contains__("Consolidated Schedule of Investments"):
            
            content = await divs[index+1].getProperty("textContent")
            text =  unicodedata.normalize('NFKC',content.toString()).replace("JSHandle:","")

            content = await  divs[index+2].getProperty("textContent")
            text +=  unicodedata.normalize('NFKC',content.toString()).replace("JSHandle:","")

            content = await  divs[index+3].getProperty("textContent")
            text +=  unicodedata.normalize('NFKC',content.toString()).replace("JSHandle:","")

            if (text.__contains__(date[0]) and
                text.__contains__(date[1]) and
                text.__contains__(date[2])):
                return divs[index::]
    return []
        
async def make_table(page,date):

    targets = []
    
    try:
        frame = await find_frame(page)

        target_frame_content = await frame.querySelector('html > body > div.reboot.main-container > #dynamic-xbrl-form')

        divs = await target_frame_content.querySelectorAll('div');

        targets = await narrow_divs(divs,date)

        
        
    except:
        print("Frame not found")

    if len(targets) == 0:

        try:
            query = "html > body > *"
            doc = await page.querySelectorAll(query)
            targets.extend(doc)

            while doc:
                targets.extend(doc)
                query +=" > *"
                doc = await page.querySelectorAll(query)
        except:
            print("Date filing not found",)
    df = pd.DataFrame()

    for target in targets:
        
        table = await target.querySelector('table > tbody')
        
        if table:

            return_rows,continue_bool = await ptab.process_table(table)
            
            df = pd.concat([df,return_rows])
            if continue_bool == False:
                print("is this found?")
                break

    return df
