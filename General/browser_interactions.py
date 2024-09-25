import asyncio
import pyppeteer as pt
import unicodedata
import pandas as pd
import pdb

import process_table as ptab

# Get text content of puppeteer element
async def element_text(element):

    content = await element.getProperty("textContent")
    
    # convert the content into a string with escape characters
    content_string = content.toString()

    # remove escape characters
    normalized_string = unicodedata.normalize('NFKC',content_string)

    # remove the JSHandle qualifier
    return_string = normalized_string.replace("JSHandle:","")
    
    return return_string

# Launch a browser instance and go to a link
async def initialize_browser(link):

    # Launch the browser and create a new page
    browser = await pt.launch({"headless" : False})
    page = await browser.newPage()

    # Go to a new link and wait for it to load
    await page.goto(link,{"waitUntil" : ['domcontentloaded',
                    'networkidle2','networkidle0'] })

    # return the page and browser
    return page,browser

# Find the iframe of the table
async def find_frame(page):

    # iterate through iFrames and look for the proper frame
    for frame in page.frames:
        if frame.name == "ixvFrame":
            return frame

    # if no table found, return none
    return None

# narrow the possible divs down so it only finds the correct table
async def narrow_divs(divs,date):

    for index,div in enumerate(divs):
        content = await div.getProperty("textContent")
        text = await element_text(content)

        if text.__contains__("SCHEDULE OF INVESTMENTS"):

            # get the 3 lines after "Consolidated Schedule of Investments
            # and check if the data is correct, then return the narrowed down divs
            # This lets the first table foudn be the correct one!
            text =  await element_text(divs[index+1])
            text +=  await element_text(divs[index+2])
            text +=  await element_text(divs[index+3])
            if (text.__contains__(date[0]) and
                text.__contains__(date[1]) and
                text.__contains__(date[2])):
                return divs[index::]

    # if divs weren't able to be narrowed, return an empty list
    return []

# create the table
async def make_table(page,date):

    # iitialize empty div list
    targets = []

    # try and find the divs within an iFrame
    try:
        frame = await find_frame(page)

        target_frame_content = await frame.querySelector('html > body > div.reboot.main-container > #dynamic-xbrl-form')

        divs = await target_frame_content.querySelectorAll('div');

        targets = await narrow_divs(divs,date)

    # if an error is thrown notify that an iFrame was not foudn
    except:
        print("Finding iFrame error")

    # if no iFrame was found
    if len(targets) == 0:

        # tell the user
        print("iFrame Not Found")

        # try getting all the elements using breadthfirst
        try:
            query = "html > body > *"
            doc = await page.querySelectorAll(query)
            targets.extend(doc)
            while doc:
                targets.extend(doc)
                query +=" > *"
                doc = await page.querySelectorAll(query)
            
        # if neither was found, tell the user
        except:
            print("Finding #document error",)

    if len(targets) == 0:
        return None

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
