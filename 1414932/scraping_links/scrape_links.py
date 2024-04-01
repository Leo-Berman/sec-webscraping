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
def extract_table(table,first_table=False, header = None):
    table_rows = table.find_all('tr')
    header_length = 0
    
    if header != None:
        header_length = len(header)
    rows = []

    for x in table_rows:
        # print(x)
        app_row = [el.text.strip() for el in x.find_all('td')]
        # print(app_row)
        if 'Portfolio Company' in app_row and header == None:
            header = app_row.copy()
            header_length = len(header)
        else:
            deletions = []
            for j in range(8,len(app_row)):
                app_row[j]=app_row[j].replace(',','')
                if "(" in app_row[j]:
                    # print("() = ", app_row[j])
                    pass
                elif app_row[j].isnumeric():
                    # print("## = ",app_row[j])
                    pass
                elif len(app_row) > header_length:
                #     print("---")
                #     print(app_row)
                    # app_row.pop(j)
                #     print(app_row)
                #     print("---")
                    # app_row[len(app_row)-1]+=note
                    deletions.append(j)
                    pass

            note_addition = ""
            while len(deletions) > 0 or len(app_row) > 13:
                deletion_index = deletions.pop(len(deletions)-1)
                print(deletion_index)
                note_addition+=app_row.pop(deletion_index)
                # note_addition += app_row.pop(deletions.pop(0)-k)
                # app_row[len(app_row)]+=note_addition
                
            print("note addition ",note_addition)
            app_row[len(app_row)-1]+=note_addition
            if header_length > len(app_row):
                for i in range(len(header)-len(app_row)):
                    app_row.insert(len(app_row)-2,"")
                    print(app_row)
                pass
            # for i in range(len(header)-len(app_row)):
            #     app_row.insert(len(app_row)-2,"")
            #     print(app_row)
            if header_length != 0:
                rows.append(app_row.copy())
        # else:
        #     rows.append(app_row).copy()
    df = pd.DataFrame(rows,columns=header)

    return df,header

def parse_filings():

    # get the absolute path of the filings_links.tsv
    #
    os.chdir('1414932')
    filings_path = os.path.abspath("filings_links.tsv")

    # read that file into a dataframe
    #
    df = pd.read_csv(filings_path, sep='\t',header = 0)

    # get rid of excess information from columns
    #
    df = df.drop(["Form type","Form description","Filing date"],axis = "columns")
    
    
    # Iterate through all links and find the 10-Qs and 10-Ks
    #
    for i in df.index:
        find_10_Qs_and_Ks(df['Filings URL'][i],df['Reporting date'][i])
    # find_10_Qs_and_Ks(df['Filings URL'][0],df['Reporting date'][0])

def find_10_Qs_and_Ks(input_URL,date):

    # read the html of the website
    #
    base = requests.get(input_URL)
    
    # convert to BeautifulSoup
    #
    soup = bs(base.content, "html.parser")

    # find the the table with the 10-Qs and 10-Ks
    #
    result = soup.find("table",attrs={"class":"tableFile"})

    # Header for holding header and rows for holding
    # the information of the table
    #
    header = []
    rows = []

    # iterate through all the rows
    #
    for i, row in enumerate(result.find_all('tr')):

        # if it is the first for, iterate through the row and 
        # set the header to a list of the header types in html
        #
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th')]

        # otherwise treat it like a normal row
        #
        else:

            # create a list to hold the row
            #
            applist = []

            # for each element in the row
            #
            for el in row.find_all('td'):

                # if there is a link get the link 
                #
                a = el.find('a')
                if a != None:
                    applist.append("https://www.sec.gov/ixviewer/ix.html?" + a.get("href")[4:])
                # otherwise append the plain text
                #
                else:
                    applist.append((el.text.strip()))

            # appen the list holding the row to the list of 
            # rows
            #
            rows.append(applist.copy())

    # convert to a dataframe
    #
    df = pd.DataFrame(rows,columns = header)

    # search by the description and index the link
    #
    resultQ = df[df["Description"]=="10-Q"]["Document"]
    resultK = df[df["Description"]=="10-K"]["Document"]
    try:
        resultQ[0] = resultQ[0].replace('hives','doc=/Archives')
        resultK[0] = resultK[0].replace('hives','doc=/Archives')
    except:
        pass
    # check to see if there is a link for each 10-Q or 10-K
    # and if so try and parse the information
    #
    try:
        parse_SOI_tables(resultQ[0],date,"Q")
    except:
        pass
    try:
        parse_SOI_tables(resultK[0],date,"K")
    except:
        pass

def parse_SOI_tables(input_URL: str,date:str,formtype:str):
    print(input_URL)
    driver = webdriver.Chrome()
    driver.get(input_URL)
    time.sleep(10)
    html = driver.page_source
    soup = bs(html,features="html5lib")
    
    First_Soi = soup.find("span", string = re.compile("Consolidated Schedule of Investments")).parent.parent.parent
    Curr_Soi_Index = First_Soi.find_all('a')
    for x in Curr_Soi_Index:
        if x.encode_contents().isdigit():
            Curr_Soi_Pgnum = int(x.encode_contents())

    Second_Soi = soup.find("span", string = re.compile("Consolidated Schedule of Investments")).findNext("span", string = re.compile("Consolidated Schedule of Investments")).parent.parent.parent
    Prev_Soi_Index = Second_Soi.find_all('a')
    for x in Prev_Soi_Index:
        if x.encode_contents().isdigit():
            Prev_Soi_Pgnum = int(x.encode_contents())
    
    iterations = Prev_Soi_Pgnum - Curr_Soi_Pgnum
    
    # Navigates to first part of table
    Titles = soup.find("span", string = re.compile("Consolidated Schedule of Investments"))
    Titles = Titles.findNext("span", string = re.compile("Consolidated Schedule of Investments"))
    Titles = Titles.findNext("span", string = re.compile("Consolidated Schedule of Investments"))
    table = Titles.findNext("table")
    df_list = []
    df,data_header = extract_table(table,first_table=True,header = None)
    print(df)
    df_list.append(df)
    
    for x in range(iterations-2):
        table = table.findNext("span", string = re.compile("Consolidated Schedule of Investments"))
        table = table.findNext("table")
        df,unused = extract_table(table,first_table=False,header = data_header)
        df_list.append(df)
    df = pd.concat(df_list,ignore_index=False, axis=0)
    print(df)
    df.to_excel("DATATOROSEN/"+date+formtype+".xlsx",index=False)
    print("past")
def main():
    parse_filings()
    pass

if __name__ == "__main__":
    main()