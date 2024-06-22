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
