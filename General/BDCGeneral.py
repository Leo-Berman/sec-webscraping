import asyncio
import pyppeteer as pt
import unicodedata

import browser_interactions as bi


async def main():
    target_url = "https://www.sec.gov/ix?doc=/Archives/edgar/data/1414932/000141493224000008/ocsl-20240331.htm"
    date = ["March","31","2024"]

    page,browser = await bi.initialize_browser(target_url)

    df = await bi.make_table(page,date)

    print(df)

    await browser.close()

    
    # write the dataframe to excel
    df.to_excel("test.xlsx",index=False)
    print("Excel Wrote")


    

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
