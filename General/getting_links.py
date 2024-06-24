import asyncio
import Helper
import pandas as pd

async def get_link_info(CIK,HEADER):

    df = Helper.fetch_filing_data(cik = CIK, headers=HEADER)
    print(df)
    if df is not None:
        return df['fileLink'].tolist(), df['reportDate'].tolist(),df['form'].tolist()

    
async def get_link_info_OLD(excel_path):
    df = pd.read_excel(excel_path,converters={'Reporting date':str})

    print(df)
    return_dates = []
    dates = df['Reporting date'].tolist()
    for x in dates:
        if type(x) != float:
            return_dates.append(x[:10])
        
    
    return df['Filings URL'].tolist(),return_dates,df['Form type'].tolist()
