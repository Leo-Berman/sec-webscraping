import asyncio
import pyppeteer as pt
import re
import unicodedata
import pandas as pd

async def process_table(table):
    #return None,False

    
    table_rows = (await table.querySelectorAll('tr'))[1::]
    print("past")
    
    rows = []

    proper_table = False
    
    for x in table_rows:
        content = await x.getProperty("textContent")
        text = unicodedata.normalize('NFKC',content.toString()).replace("JSHandle:","")
        if text.__contains__("Portfolio Company"):
            proper_table = True
            break

    if proper_table == False:
        return pd.DataFrame(),True
    
    for x in table_rows:
        cells = await x.querySelectorAll('td')
        row_elements = [""]
        for y in cells:

            if y:
                content = await y.getProperty("textContent")
                text = unicodedata.normalize('NFKC',content.toString()).replace("JSHandle:","")
                
                if text.__contains__("Total Non-Control"):
                    return pd.DataFrame(rows),False
                
                boxsize = (await y.boundingBox())

                if boxsize:
                    width = boxsize['width']
                    
                    if width > 20:
                        if (len(row_elements) == 1) and (row_elements[0] == ""):
                            row_elements[0] = text
                        else:
                            row_elements.append(text)
                else:
                        row_elements[len(row_elements)-1]+=text
        rows.append(row_elements)

    for i in range(len(rows)):
        if len(rows[i]) != len(rows[i]):
            print("Houston, we have a problem")

    print(pd.DataFrame(rows))
            
    return pd.DataFrame(rows),True

async def main():
    browser = await pt.launch({"headless" : False})
    page = await browser.newPage()

    await page.goto("https://www.sec.gov/ix?doc=/Archives/edgar/data/1414932/000141493224000008/ocsl-20240331.htm",
                    { "waitUntil" : ['domcontentloaded','networkidle2','networkidle0'] })

    # print(dir(page))
    # print(dir(page.frames))

    frames = page.frames

    target_frame_url = "https://www.sec.gov/ixviewer/ix.html?doc=/Archives/edgar/data/1414932/000141493224000008/ocsl-20240331.htm"
    
    target_frame = None
    
    for frame in frames:
        if frame.url == target_frame_url:
            target_frame = frame
            break
    print("1 - ",type(target_frame))
    print(dir(target_frame))

    target_frame_content = await target_frame.querySelector('html > body > div.reboot.main-container > #dynamic-xbrl-form')

    target_frame_content_divs = await target_frame_content.querySelectorAll('div');

    for index,div in enumerate(target_frame_content_divs):
        content = await div.getProperty("textContent")
        text = content.toString()
        if text.__contains__("Consolidated Schedule of Investments"):

            content = await target_frame_content_divs[index+1].getProperty("textContent")
            text = content.toString()
            #print("in-1")

            #print(text)
            
            #regexp = re.compile(r'March.*31.*2024;')
            #if regexp.search(text):

            if (text.__contains__("March") and
                text.__contains__("31") and
                text.__contains__("2024")):
                print(text)
                print(index)
                found = index
                break


            
    
    found = 0
            
    targets = target_frame_content_divs[220::]

    df = pd.DataFrame()
    
    for x in targets:
        table = await x.querySelector('table > tbody')
        
        
        
        if table:

            return_rows,continue_bool = await process_table(table)
            
            df = pd.concat([df,return_rows])
            if continue_bool == False:
                print("is this found?")
                break


           








    
    
    '''table = await target_frame_content_divs[126].querySelector('table')
    content = await table.getProperty("textContent")
    text = content.toString()'''
    
    #target_frame_content_text = await target_frame_content.getProperty("textContent")

    #target_frame_content_text_json_value = target_frame_content_text.toString()
    #print("3 - ",target_frame_content_text_json_value.encode('utf8'))
    

    await browser.close()

    
    # write the dataframe to excel
    df.to_excel("test.xlsx",index=False)

    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
