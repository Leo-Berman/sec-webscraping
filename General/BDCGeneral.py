import asyncio 
import calendar
import getting_links as gl
import browser_interactions as bi
import pandas as pd
from common_error import custom_error

global_file_name = "BDCGeneral.py"

# split the date into a list that has the actual name of the month
async def split_date(date):
    date = date.split("-")
    return [calendar.month_name[int(date[1])], date[2], date[0]]

# search the file for the Consolidated Schedule of Investmenets
# table
async def do_filing(target_url,old_date,form,CIK):

    # Get the date into a list that has the actual name of the month
    date = await split_date(old_date)

    # get the filing open
    page,browser = await bi.initialize_browser(target_url)

    # make the table
    df = await bi.make_table(page,date)

    # close the browser
    await browser.close()

    # if table wasn't found tell the user
    if type(df) != pd.DataFrame:
        print("Type Error, no table found")
        return False
    elif df.empty:
        print("Table empy, no table found")
        return False
    
    # otherwise write the dataframe to excel
    else:
        with pd.ExcelWriter(CIK + "/" + CIK + ".xlsx",
                            mode = "a", engine="openpyxl",
                            if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=old_date, index=False)

        return True

async def main():

    # enter the ticker and the header
    CIK =  '000' + '0878932'
    HEADER = {'User-Agent' : 'BDC Researcher'}

    # get the filing metadta
    links,dates,forms = await gl.get_link_info(CIK,HEADER)
    
    if len(links) == len(dates) == len(forms) != 0:
        print("Links successfully retrieved")
    else:
        common_error(global_file_name,
                     main.__name__,
                     "Links weren't able to be retrieved")

    # write those links to an excel sheet
    df = pd.DataFrame( {
        'dates': dates,
        'form types': forms,
        'links': links
        })
    df.to_excel(CIK + "/" + CIK+ "_links.xlsx",index=False)

    # iterate through each filing
    i = 0
    for link,date,form in zip(links,dates,forms):

        # tell the user there is a new filing being processed
        print("New Filing\n\n","Formtype = ",form,"\n","Date = ",date,"\n\n")

        # get the soi table
        complete_bool = await do_filing(link,date,form,CIK)

        # notify the user if the filing was completed successfully
        # or unsuccessfully
        i+=1
        print("\n\n", i,
              "/",len(links),
              "Filing Completed",
              "successfully" if complete_bool == True else "unsuccessfully")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
