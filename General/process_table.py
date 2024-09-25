import asyncio
import pyppeteer as pt
import re
import unicodedata
import pandas as pd
import common_error as ce
import browser_interactions as bi


# check to make sure the table is actually the table we're looking for
async def check_proper_table(table_rows):

    # iterate through all the rows in the table
    for row in table_rows:

        # check if the row has "Portfolio Company" in it, this notifies us
        # that this is the proper table
        text = await bi.element_text(row)
        if text.__contains__("Portfolio Company"):
            return True

    # otherwise say it isn't a proper table
    return False

# process a single row
async def process_row(row):

    continue_bool = True
    
    # get all cells in a row and initialize a return list
    cells = await row.querySelectorAll('td')
    row_elements = [""]

    # iterate through all the cells in the row
    for cell in cells:

        # if cell exists
        if cell:

            # get the cell text
            text = await bi.element_text(cell)

            # if end of table return the dataframe and tell the program to stop
            if text.__contains__("Total Investents"):
                continue_bool = False

            # get the graphical size of the box
            boxsize = (await cell.boundingBox())

            # if successful
            if boxsize:

                # get the width of the element
                width = boxsize['width']

                # if it's big enough append it
                if width > 20:
                    if (len(row_elements) == 1) and (row_elements[0] == ""):
                        row_elements[0] = text
                    else:
                        row_elements.append(text)

                # otherwise add it to the last cell
                else:
                    row_elements[len(row_elements)-1]+=text
    return row_elements,continue_bool

async def check_row_lengths(rows):
    FILE = "process_table.py"
    FUNCTION = "check_row_lengths"
    for i in range(len(rows)-1):
        if len(rows[i]) != len(rows[i+1]):
            ce.custom_error(FILE, FUNCTION, "Row lengths are different")
            
async def process_table(table):
    FILE = "process_table.py"
    FUNCTION = "process_table"

    # Find all table row elements and initialize an empty list
    table_rows = (await table.querySelectorAll('tr'))[1::]
    return_rows = []

    # Check to see it is the table we are looking for
    # If it isn't, return an empty dataframe and continue
    proper_table = await check_proper_table(table_rows)
    if proper_table == False:
        return pd.DataFrame(),True

    
    cont_bool = True
    

    # iterate through the rows and process them
    for row in table_rows:
        row_elements,continue_bool = await process_row(row)
        if (continue_bool == False):
            cont_bool = False    
        return_rows.append(row_elements)

        
    # return a dataframe of the rows
    return pd.DataFrame(return_rows),cont_bool
