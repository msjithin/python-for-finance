import pandas as pd 

def get_tax(country='France'):
    tax_df = pd.read_csv('personal income tax.csv')
    tax_row = tax_df[tax_df['Country'] == country]
    return tax_row['Last'].values[0]

def get_total(income=1, rate1=0, rate2=0, rate3=0):
    return round(income * ( 1 + rate1/100 + rate2/100 + rate3/100 ), 2 )

if __name__ == '__main__':
    print( get_tax() )
    print( get_total(100, 3,2,2))