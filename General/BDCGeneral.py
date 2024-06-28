import asyncio 
import calendar
import getting_links as gl
import browser_interactions as bi

async def split_date(date):
    date.split("-")
    
    return_date = []
    
    return_date.append(calendar.month_name[int(date[1])])
    return_date.append(date[2])
    return_date.append(date[0])

    return return_date

async def do_filing(target_url,old_date,form,CIK):

    date = await split_date(old_date)
    
    page,browser = await bi.initialize_browser(target_url)

    df = await bi.make_table(page,date)

    print(df)

    await browser.close()

    
    # write the dataframe to excel
    df.to_excel(CIK + "/" + CIK+ "_" +old_date + "_" +
                form + ".xlsx",index=False)
    print("Excel Wrote")


async def main():
    #CIK = '0001414932'
    #CIK = '0001268752'
    CIK =  '0001513363'
    HEADER = {'User-Agent' : 'IITSAME'}
    links,dates,forms = await gl.get_link_info(CIK,HEADER)
    
    #CIK = '0001268752'
    
    #links,dates,forms = await gl.get_link_info("test.xlsx")
    for link,date,form in zip(links,dates,forms):

        await do_filing(link,date,form,CIK)
    

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
