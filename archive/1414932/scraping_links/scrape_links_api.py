from sec_api import QueryApi
def main():
    queryApi = QueryApi(api_key="77dde58c2f84509f33022c654276d13491eb37a21f39da83c89b938257c852ae")

    query = {
      "query": { "query_string": { 
          "query": "formType:(\"10-K\",\"10-Q\") AND ticker:OCSL", # only 10-Ks and Qs
      }},
      "from": "0", # start returning matches from position null, i.e. the first matching filing 
    }

    response = queryApi.get_filings(query)
    print(response)
if __name__ == "__main__":
    main()
