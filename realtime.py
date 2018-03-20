
import csv
import datetime
import re
import io
import pandas as pd
import requests
from datetime import datetime, timedelta
df_realTime =pd.DataFrame()

def get_google_finance_intraday(ticker, period=60, days=3):


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
        #print(row)
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            
            else:
                
                times.append(start+timedelta(seconds=period*int(row[0])))
            rows.append(map(float, row[1:]))
    #print(len(rows))
    
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
yesterday = datetime.now() - timedelta(days=1)
today = datetime.now()
Ydatex=yesterday.strftime('%Y-%m-%d %H:%M:00')
Tdatex=today.strftime('%Y-%m-%d %H:%M:00')
#print(Ydatex)
#print(Tdatex)
print("Generating Real Time Data:\n")
for i in List:
    #print(i)
    df = (get_google_finance_intraday(i, period=60, days=3))
    df=df.ix[Ydatex:Tdatex]
    df.to_csv(str(i) + "_real.csv")
    df_realTime=df_realTime.append(df)
    #print(len(df))
#print(len(df_realTime))
df_realTime
# a for loop to get the HISTORICAL DATA  stock data of each company in the list ,and
# saving it in the csv file.

# connecting to database and creating the table and inserting rows

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

from pandas.io import sql
from sqlalchemy import create_engine
import MySQLdb as db

db1 = MySQLdb.connect(host="localhost",user="root",passwd="give your passwd")
cursor = db1.cursor()
sql = 'CREATE DATABASE realtime_data'
cursor.execute(sql)
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="type your passwd",
                               db="realtime_data"))






df_realTime.to_sql(con=engine, name='realtime_data', if_exists='replace')








