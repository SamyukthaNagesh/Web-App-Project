import csv
import datetime
import re
import xlrd
import pandas as pd
import requests

def get_google_finance_intraday(ticker, period=60, days=1):
    

    uri = 'https://finance.google.com/finance/getprices' \
          '?i={period}&p={days}d&f=d,o,h,l,c,v&df=cpct&q={ticker}'.format(ticker=ticker,
                                                                          period=period,
                                                                          days=days)
    
    page = requests.get(uri)
    reader = csv.reader(page.text.splitlines())
    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    rows = []
    times = []
    for row in reader:
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start+datetime.timedelta(seconds=period*int(row[0])))
            rows.append(map(float, row[1:]))
    if len(rows):
        ##return ''.join(["{0},{1},{2},{3},{4}\n".rows, pd.DatetimeIndex(times, name = 'Date'), colummns])
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'),
                            columns=columns)
    else:
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))
        
        


##print(get_google_finance_intraday('BN', period=60*60*24, days=365))

f = open("stocks.csv",'w')

List = ['AABA','AMC','AMD','BN','GOOG','GPS','HTZ','NTDOY','PYPL','WFC']

for i in List:
    print(i)
    print(get_google_finance_intraday(i, period=60, days=1))
    f.write
    print('######## ######## ######## ######## ######## ######## ########')
    
