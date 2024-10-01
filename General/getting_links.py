import asyncio
import Helper
import pandas as pd
from common_error import custom_error

global_file_name = "getting_links.py"

async def get_link_info(CIK,HEADER):
    # Get the pandas datafram containing a companies 10 Ks and Qs metadata
    try:
        df = Helper.fetch_filing_data(cik = CIK, headers=HEADER)
    except:
        custom_error.custom_error(global_file_name,
                                  get_link_info.__name__,
                                  "Filing links, dates, " +
                                  "and formtype search failed")

    return (df['fileLink'].tolist(),
            df['reportDate'].tolist(),
            df['form'].tolist())
    
