from bs4 import BeautifulSoup as bs
import os
import pandas as pd
import requests
import time
import requests_random_user_agent
import re
import numpy as np
def parse_filings():
    filings_path = os.path.abspath("filings_links.tsv")
    df = pd.read_csv(filings_path, sep='\t',header = 0)
    df = df.drop(["Form type","Form description","Filing date"],axis = "columns")
    
    '''
    Iterate through all links temporarily disabled
    for i in df.index:
        open_link(df['Filings URL'][i])
        time.sleep(10)
    '''
    open_link(df['Filings URL'][0])

def open_link(input_URL):
    base = requests.get(input_URL)
    soup = bs(base.content, "html.parser")
    result = soup.find("table",attrs={"class":"tableFile"})
    header = []
    rows = []
    for i, row in enumerate(result.find_all('tr')):
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th')]
        else:
            # rows.append([el.text.strip() 
            for el in row.find_all('td')]):
                el.find('a')
                pass
    df = pd.DataFrame(rows,columns = header)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.precision', 3,):
        print(df)
    time.sleep(10)
    pass
def main():
    parse_filings()
    pass

if __name__ == "__main__":
    main()