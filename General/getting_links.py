import asyncio
import Helper
import pandas as pd
import common_error as ce

async def get_link_info(CIK,HEADER):

    FILE = "getting_links.py"
    FUNCTION = "get_link_info"
    # Get the pandas datafram containing a companies 10 Ks and Qs metadata
    try:
        df = Helper.fetch_filing_data(cik = CIK, headers=HEADER)
    except:
        ce.custom_error(FILE,FUNCTION,"Filing links, dates, and formtype search failed")

    return df['fileLink'].tolist(), df['reportDate'].tolist(),df['form'].tolist()
    
