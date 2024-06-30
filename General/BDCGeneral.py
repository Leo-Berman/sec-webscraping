import asyncio 
import calendar
import getting_links as gl
import browser_interactions as bi

async def split_date(date):
    date = date.split("-")
    return [calendar.month_name[int(date[1])], date[2], date[0]]

async def do_filing(target_url,old_date,form,CIK):

    date = await split_date(old_date)
    
    page,browser = await bi.initialize_browser(target_url)

    df = await bi.make_table(page,date)

    await browser.close()

    
    # write the dataframe to excel
    df.to_excel(CIK + "/" + CIK+ "_" +old_date + "_" +
                form + ".xlsx",index=False)


async def main():
    CIK =  '0001513363'
    HEADER = {'User-Agent' : 'ITSAME'}
    links,dates,forms = await gl.get_link_info(CIK,HEADER)
    print("Past links")

    i = 0
    for link,date,form in zip(links,dates,forms):

        await do_filing(link,date,form,CIK)
        i+=1
        print(i,"Done")
    

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
