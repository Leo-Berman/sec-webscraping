import asyncio
import Helper
import pandas as pd

async def get_link_info(CIK,HEADER):

    df = Helper.fetch_filing_data(cik = CIK, headers=HEADER)
    
    if df is not None:
        return (df['fileLink'].tolist(), df['reportDate'].tolist(),
                df['form'].tolist())

    
