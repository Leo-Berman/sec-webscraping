from bs4 import BeautifulSoup as bs
import os
import pandas as pd
import requests
import time
def parse_filings():
    filings_path = os.path.abspath("filings_links.tsv")
    df = pd.read_csv(filings_path, sep='\t',header = 0)
    df = df.drop(["Form type","Form description","Filing date"],axis = "columns")
    
    '''
    Iterate through all links temporarily disabled
    for i in df.index:
        open_link(df['Filings URL'][i])
    '''
    open_link(df['Filings URL'][0])

def open_link(input_URL):
    headers = {
        "User-Agent": "Temple University leo.berman@temple.edu",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.sec.gov"
    }
    base = requests.get(input_URL,headers)
    soup = bs(base.content, "html.parser")
    result = soup.find("title")
    print(result.prettify())
    time.sleep(10)
    pass
def main():
    parse_filings()
    pass

if __name__ == "__main__":
    main()