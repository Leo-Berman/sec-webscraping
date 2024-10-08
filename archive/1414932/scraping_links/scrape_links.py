#!/usr/bin/env python3
from bs4 import BeautifulSoup as bs
import os
import pandas as pd
import requests
import time
import requests_random_user_agent
import re
import numpy as np
import time
from pathlib import Path
from selenium import webdriver
def extract_table(table,date,first_table=False, header = None):
    
    # find all the rows in the table
    table_rows = table.find_all('tr')
    
    # get the header_length
    header_length = 0
    if header != None:
        header_length = len(header)
    
    # create a list for storing rows
    rows = []

    goodrows = 9
    if date == "2023-12-31" or date=="2023-09-30" or date=="2023-06-30" or date=="2023-03-31" or date=="2022-12-31":
        goodrows=9
    else:
        return None,False
    # iterate through all the rows
    for x in table_rows:


        # get all row elements 
        app_row = [el.text.strip() for el in x.find_all('td')]
        
        # check if it is the end of the table and if so return
        #print(app_row[0])
        if 'Total Non-Control' in app_row[0]:
            df = pd.DataFrame(rows,columns=header)
            #print('asdklaslkjd')
            return df,False
        
        # if this is the beginning of the page of the table
        if 'Portfolio Company' in app_row[0]:
            pass


        else:
            # create a list for holding extraneous character positions
            deletions = []

            # iterate through the ending bits of the row
            for j in range(goodrows,len(app_row)):

                # replace all commas with nothing so we can check if it is a number
                app_row[j]=app_row[j].replace(',','')

                # check to see if a note is in the cell
                if "(" in app_row[j]:
                    pass

                # check to see if it is a number
                elif app_row[j].isnumeric():
                    pass

                # if it is none of those things and the row is too long start marking deletions 
                elif len(app_row) > header_length:
                    deletions.append(j)
                    pass

            # create a string for holding the appendment to the notes section
            # this will hold all extraneous characters 
            note_addition = ""


            while len(deletions) > 0 or len(app_row) > 13:
                deletion_index = deletions.pop(len(deletions)-1)
                note_addition+=app_row.pop(deletion_index)
            app_row[len(app_row)-1]+=note_addition
            if header_length > len(app_row):
                for i in range(len(header)-len(app_row)):
                    app_row.insert(len(app_row)-2,"")
                pass

            if "—" in note_addition and app_row[2] == "Common Stock":
                app_row[8] = app_row[11]
                app_row[11] = ""
            elif ("—" not in note_addition and app_row[2] == "Preferred Equity") or ("—" not in note_addition and app_row[2] == "Common Stock"):
                app_row[10] = app_row[9]
                app_row[9] = ""
            elif "—" in note_addition and  app_row[2] == "Membership Interest":
                app_row[8] = app_row[11]+"%"
                app_row[11] = ""

            elif "—" not in note_addition and  app_row[2] == "Membership Interest":
                app_row[10] = app_row[9]
                app_row[9] = ""
                app_row[8]+= "%"

            elif note_addition.count("—")==2 and  app_row[2] == "Warrants":
                app_row[8] = app_row[11]
                app_row[11] = ""

            elif note_addition.count("—")==0 and  app_row[2] == "Warrants":
                app_row[10] = app_row[9]
                app_row[9] = ""

            
            
            
            if header_length != 0 and ("Total" not in app_row[0]):
                rows.append(app_row.copy())
    
    df = pd.DataFrame(rows,columns=header)

    return df,True

def read_links(inputfile):
    df = pd.read_excel(inputfile)
    return df['fileLink'].tolist(), df['reportDate'].tolist(), df['form'].tolist()

def parse_SOI_table(input_URL: str,date:str,formtype:str,com_header:list):
    # opens up the link and extracts the html
    #print(input_URL)
    driver = webdriver.Chrome()
    driver.get(input_URL)
    time.sleep(10)
    html = driver.page_source
    soup = bs(html,features="html5lib")


    # Manually input the start of the tables
    
    if date == "2023-12-31":
        pagenum = 5
    elif date == "2023-09-30":
        pagenum = 86
    elif date == "2023-06-30":
        pagenum = 6
    elif date == "2023-03-31":
        pagenum = 6
    elif date == "2022-12-31":
        pagenum = 6
    else:
        return
    soi_loc = soup.find_all("hr")[pagenum]

    # Find the table
    soi_table_html = soi_loc.find_next("table")
    
    # Variable for when it finds those extraneous variables
    cont = True

    # List for holding the tables
    soi_table_list = []

    # extract the table
    table,cont=extract_table(soi_table_html,date,first_table = True, header = com_header)
    
    # append the dataframe to the list and find the next table
    soi_table_list.append(table)
    soi_table_html = soi_table_html.find_next("table")

    # while the cont variable is true, keep parsing tables
    while cont:
        table,cont=extract_table(soi_table_html,date,first_table = False, header = com_header)
        soi_table_list.append(table)
        soi_table_html = soi_table_html.find_next("table")

    # get all the data frames in 1 dataframe
    df = pd.concat(soi_table_list,ignore_index=False, axis=0)

    # write the dataframe to excel
    df.to_excel("DATATOROSEN/"+date+"_"+formtype+".xlsx",index=False)

def main():
    
    links,dates,formtype = read_links("OAKTREE_Filing_Data.xlsx")
    common_header = ['Portfolio Company','Industry','Type of Investments','Index','Spread','Cash Interest','PIK','Maturity Date','Shares','Principal','Cost','Fair Value','Notes']
    # retry_parse_SOI_table(links[0],dates[0],formtype[0],common_header)

    # for testing because everything after might be worth doing by hand
    links = links[0:53]
    dates = dates[0:53]
    formtype = formtype[0:53]
    # end
    
    for link,date,form in zip(links,dates,formtype):
        print(link,date)
        parse_SOI_table(link,date,form,common_header)

if __name__ == "__main__":
    main()
