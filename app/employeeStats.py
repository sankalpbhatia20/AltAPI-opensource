import pandas as pd

def company_employee_statistics(asset):
    '''Use web scrapping to extract employee statistics of the entered company'''
    df = pd.read_html('https://www.glassdoor.co.in/Reviews/{}-Reviews-E43129.htm'.format(asset,asset))
    print(df)

company_employee_statistics('Tesla')