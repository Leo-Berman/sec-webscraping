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
def extract_table(table):
    table_rows = table.find_all('tr')
    # print(table_rows)
    rows = []
    headers = []
    # print(table.prettify())
    for i,x in enumerate(table_rows):
        if i == 0:
            pass
        elif i == 1:
            headers = [el.text.strip() for el in x.find_all('td')]
        else:
            rows.append([el.text.strip() for el in x.find_all('td')])
        
    df = pd.DataFrame(rows,columns = headers)
    # print(len(rows))
    print(df.to_string())

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
    # for i in df.index:
    #     find_10_Qs_and_Ks(df['Filings URL'][i]),df['Reporting date'][i]
    find_10_Qs_and_Ks(df['Filings URL'][0],df['Reporting date'][0])

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

    # check to see if there is a link for each 10-Q or 10-K
    # and if so try and parse the information
    #
    try:
        parse_SOI_tables(resultQ[0],date)
    except:
        pass
    try:
        parse_SOI_tables(resultK[0],date)
    except:
        pass

def parse_SOI_tables(input_URL: str,date):
    print(input_URL)
    driver = webdriver.Chrome()
    driver.get(input_URL)
    time.sleep(10)
    html = driver.page_source
    soup = bs(html,features="html5lib")
    Titles = soup.find("span", string = re.compile("Consolidated Schedule of Investments"))
    Titles = Titles.findNext("span", string = re.compile("Consolidated Schedule of Investments"))
    Titles = Titles.findNext("span", string = re.compile("Consolidated Schedule of Investments"))
    table = Titles.findNext("table")
    extract_table(table)
def main():
    parse_filings()
    pass

if __name__ == "__main__":
    main()