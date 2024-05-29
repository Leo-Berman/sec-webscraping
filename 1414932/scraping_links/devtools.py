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
from selenium.webdriver.common.by import By
def extract_table(table,date,seldrive,first_table=False, header = None):
    
    # find all the rows in the table
    table_rows = table.find_all('tr')
    
    # get the header_length
    header_length = 0
    if header != None:
        header_length = len(header)
    
    # create a list for storing rows
    rows = []

    for x in table_rows:
        Type = x.name
        Attrs = x.attrs
    
    df = pd.DataFrame(rows,columns=header)

    return df,True

def read_links(inputfile):
    df = pd.read_excel(inputfile)
    return df['fileLink'].tolist(), df['reportDate'].tolist(), df['form'].tolist()

def parse_SOI_table(input_URL: str,date:str,formtype:str,com_header:list):
    # opens up the link and extracts the html
    driver = webdriver.Chrome()
    driver.get(input_URL)

    
    time.sleep(10)
    pagebreaks = driver.find_elements(By.TAG_NAME, 'hr')
    
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
        # If it doesn't find anything then error out and notify user #        
        return

    soi_loc = soup.find_all("hr")[pagenum]

    # Find the table
    soi_table_html = soi_loc.find_next("table")
    
    # Variable for when it finds those extraneous variables
    cont = True

    # List for holding the tables
    soi_table_list = []

    # extract the table
    table,cont=extract_table(soi_table_html,date,driver,first_table = True, header = com_header)
    
    # append the dataframe to the list and find the next table
    soi_table_list.append(table)
    soi_table_html = soi_table_html.find_next("table")

    # while the cont variable is true, keep parsing tables
    while cont:
        table,cont=extract_table(soi_table_html,date,driver,first_table = False, header = com_header)
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
        if link == links[0]:
            break

if __name__ == "__main__":
    main()
