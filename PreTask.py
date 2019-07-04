#6/29/2019 Chaoyi
#'pip install pandas-datareader'
#'pip install yfinance --upgrade --no-cache-dir' 
import datetime
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as pdr
import yfinance as yf
yf.pdr_override()
from  pandas import Series, DataFrame

#read data from csv or excel
#requires that first column is tickes, second column is weights/...
#and first row are titles of columns
def ReadFile(fileName) :

    if fileName[fileName.rfind(".")+1:] == 'csv':
        df = pd.read_csv(fileName)
    elif fileName[fileName.rfind(".")+1:] == 'xlsx':
        df = pd.read_excel(fileName)
    else : return'Wrong File Type'

    df.dropna(axis=0,how='any') #drop all rows that have any NaN values
    return df

#used to get prices ready accordingly from Yahoo Finance
#parameter dataframe: tickers & weights/...
def GetPrice(dataframe, start_date, end_date):

    Names = dataframe.iloc[:,0] #first column

    tickerList = Names.array #convert Series to array

    #retrieve data from yahoo finance
    all_data = {}
    for ticker in tickerList:
        all_data[ticker] = pdr.get_data_yahoo(ticker, start_date, end_date)

    #store data in DataFrame
    price = DataFrame({tic: data['Adj Close']
                        for tic, data in all_data.items()})

    return price


if __name__ == '__main__':
    #should be connected to user input
    fileName = 'test.csv'
    start = datetime.date(2019, 1, 1)#resolve if only input year later
    end = datetime.date(2019, 2, 1)
    df = ReadFile(fileName)
    price = GetPrice(df, start, end)
    print(price)
