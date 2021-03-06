import csv
import datetime
import re
import io
import pandas as pd
import requests

# ticker = company ticker
# period = time in seconds from one data to other.
# days = no of days.

def get_google_finance_intraday(ticker, period=60, days=1):


    url = 'https://finance.google.com/finance/getprices' \
          '?i={period}&p={days}d&f=d,o,h,l,c,v&df=cpct&q={ticker}'.format(ticker=ticker,
                                                                          period=period,
                                                                          days=days)

    page = requests.get(url)
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
        result = pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'), columns=columns)
        result.insert(0, 'Ticker', ticker)
        return result
    else:
        result = pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))
        result.insert(0, 'Ticker', ticker)
        return result




# the companies we are considering to extract the data is in the list


List = ['AABA','AMC','AMD','BN','GOOG','GPS','HTZ','NTDOY','PYPL','WFC']

# a for loop to get the REAL TIME stock data of each company in the list ,and
# saving it in the csv file.

print("Generating Real Time Data:\n")
for i in List:
    #print(i)
    df = (get_google_finance_intraday(i, period=60, days=1))
    df.to_csv(str(i) + '_real.csv')
    #print(df)

# a for loop to get the HISTORICAL DATA  stock data of each company in the list ,and
# saving it in the csv file.

print("Generating Historical Time Data:\n")

import datetime
now = datetime.datetime.now()

for i in List:
    #print(i)
    df = "http://finance.google.com/finance/historical?q="+str(i)+"&startdate= "+ str(now.month) + "2017&enddate= " + str(now.month) +"2018&num=200&output=csv"
    raw_response = requests.get(df).content
    stock_data = pd.read_csv(io.StringIO(raw_response.decode('utf-8')))
    stock_data.to_csv(str(i)+'_hist.csv',index=False)
