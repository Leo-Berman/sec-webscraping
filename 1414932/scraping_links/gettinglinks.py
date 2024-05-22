import Helper
import pandas as pd
def main():

    CIK =  '0001414932'
    HEADER = {
        'User-Agent': 'Oaktree Lending BDC, Inc.'
    }
    filing_data = Helper.fetch_filing_data(cik = CIK, headers=HEADER)
    
    if filing_data is not None:
        file_name="OAKTREE_Filing_Data.xlsx"
        with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
            filing_data.to_excel(writer, index=False)
            worksheet=writer.sheets['Sheet1']
            for i, col in enumerate(filing_data.columns):
                column_len=max(filing_data[col].astype(str).str.len().max(), len(col)) +2
                worksheet.set_column(i, i, column_len)

        filing_links=Helper.get_filing_links(file_name)
        print(filing_links)

if __name__ == "__main__":
    main()