import asyncio
import Helper
import pandas as pd

async def get_link_info(CIK,HEADER):

    filing_data = Helper.fetch_filing_data(cik = CIK, headers=HEADER)
    
    if filing_data is not None:
        print(filing_data)

if __name__ == "__main__":
    main()
