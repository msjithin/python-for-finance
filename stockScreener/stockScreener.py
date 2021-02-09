from config import *
import requests, time, re, pickle
import os
import pandas as pd

url = 'https://api.tdameritrade.com/v1/instruments'

df = pd.read_excel('company_list.xlsx', engine='openpyxl')
symbols = df['Symbol'].values.tolist()
files_list = []


def get_data():
    start, end = 0, 500
    while start < len(symbols):
        tickers = symbols[start:end]
        payload = {'apikey':ameritrade_key,
            'symbol':tickers,
            'projection':'fundamental'
            }
        results = requests.get(url, params=payload)
        data = results.json()
        filename = time.asctime() + '.pkl'
        filename = re.sub('[ :]', '_', filename)
        files_list.append(filename)
        with open(filename, 'wb') as file:
            pickle.dump(data, file) 
        time.sleep(1)
        start = end
        end += 500
        if end > len(symbols):
            end = len(symbols)


get_data()

data = []
print('Files created : ', files_list)
for file in files_list:
    with open(file, 'rb') as f:
        info = pickle.load(f)
    tickers = list(info)
    points = ['symbol', 'netProfitMarginMRQ', 'peRatio', 'pegRatio', 'high52' ]
    for ticker in tickers:
        tick = []
        for point in points:
            tick.append(info[ticker]['fundamental'][point])
        data.append(tick)
    os.remove(file)


points = ['symbol', 'Margin', 'PE', 'PEG', 'high52']

df_results = pd.DataFrame(data, columns=points)

# Choose only stock with PEG > 1
#df_peg = df_results[df_results['PEG'] > 1]

# Choose probably good stocks
df_peg = df_results[  (df_results['PEG'] < 1 )
                    & (df_results['PEG'] > 0 )
                    & (df_results['Margin'] > 20 )
                    & (df_results['PE'] > 10 )
                   ]
df_peg = df_peg.sort_values(['PEG'])
#print(df_peg)

def view(size):
    start, stop = 0, size
    while stop < len(df_peg):
        print(df_peg[start:stop])
        start = stop
        stop += size
    print(df_peg[start:stop])
    

#view(10)










