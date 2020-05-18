#Final Project Intro to App - Patrick Calhoun
#This program at its core gathers data for stocks that are either entered by the user or loaded from file and displays them in 2 types of graphs
#the default graph which keeps track of the markets Adjusted Close for each index which is the normal representation one would see for a graph of stock price
#the other is a OpenHighLowClose Graph commonly known as a candlestick chart which displays the data in a very informative 
#and useful way for traders and analysts, with matching volume of the stock represented below
#
#!!!!!!!!!!! DO NOT RUN THIS PROGRAM IN IDLE, IT WILL STOP RESPONDING AND CRASH PYTHON WHEN LOADING CHARTS !!!!!!
#!!!!!!!!!!! IT DOES WORK IF YOU OPEN THE .py DIRECTLY WITH THE Python.exe !!!!!!
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
#date and time
import datetime as datetime
import time
import matplotlib.dates as mdates
import matplotlib.dates as date2num

#loading bar and cosmetic
import progressbar

#to show files in directory
import os

#to build a basic gui
from graphics import *

#math and numbers
import numpy as np
from math import *

#chart building
import matplotlib
matplotlib.use("TkAgg")#sets the backend
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.ticker as ticker
#very useful data analysis library
import pandas as pd

#allows ease of use with yahoo finance api(or other sleected api - however I'm using yahoo for this project)
import pandas_datareader.data as web

#candlestick chart building
from mplfinance.original_flavor import candlestick2_ohlc
from mplfinance.original_flavor import candlestick_ohlc

#Functions
def makeCsv(data, name):
    dataFrame = data
    tickerCsv = name
    
    #if directory does not exist, create it
    if not os.path.exists('CsvFolder'):
        os.makedirs("CsvFolder")

    #if exists do print message, else create csv file
    if os.path.exists("CsvFolder/"+tickerCsv+".csv"):
        print("already have:",tickerCsv)
    else:
        #dataFrame['Data'] = dataFrame['Date'].astype(mdates.date2num)
        dataFrame.to_csv("CsvFolder/"+tickerCsv+".csv")
        return

def showTickList():
    #print out a list of tickers from file
    file = open('S&P500.txt', "r")
    for line in file:
        print(line)
    return

def showPlot():
    #final call to show and setup all frames
    plt.ion() #orginal method break and pass werent working so program would freeze at show(), I found that this way worked around that issue
    plt.show()
    plt.pause(0.001)
    input("\nPress [enter] to continue.")
    plt.close('all')
    return

def defaultIt(data, inc, name, useCsv):
    tickName = name
    increment = inc


    df = data
    
    #matplot figure allows for multiple instances/windows to be made
    plt.figure(increment)
    plt.suptitle(tickName)

    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)

    #format the y axis ticker to represent dollars
    formatter = ticker.FormatStrFormatter('$%1.2f')
    ax1.yaxis.set_major_formatter(formatter)
    
    for tick in ax1.yaxis.get_major_ticks():
        tick.label1.set_visible(False)
        tick.label2.set_visible(True)

    #sets ticker to the left side
    ax1.yaxis.tick_left()
    ax1.yaxis.set_label_position("left")

    #maximizes window
    #this backend is: TkAgg
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())

    plt.xlabel("Date")
    plt.ylabel("Price")
    
    df['Adj Close'].plot(color="#57e1a4")
    plt.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.4)
    return

def loadFile(fileName):
    csvRead = 0
    print("Loading from file:", fileName)

    try:
        file = open(fileName,"r")
    except:
        print('ERROR could not load file!')
        main()

    d = {} #make a dictionary

    for line in file:
        startD, endD, tickerT = line.split(",")
        startD = startD.strip()
        endD = endD.strip()
        tickerT = tickerT.strip()
        key = tickerT
        d.setdefault(key, [])
        d[key].append(startD)
        d[key].append(endD)
        print(d.keys(), d[key])

    file.close()
    if(input("Try to load from csv?(Y/N):").upper()=='Y'):
        csvRead = 1
    mainFromFile(d, csvRead)

def addIt(stockName, startingDate, endingDate):
    #writes the start date, end-date, and ticker to file seperated by commas so that it can be delimitid and read back in for later use
    myfile = open(input("Enter filename to save to:"), "a+")
    myfile.write(str(startingDate) + "," + str(endingDate) + "," + str(stockName) + "\n")

    print("file saved")

def csvCandle(data, inc, name):
    #CSV version - volume and dates are broken
    print("-----loading from csv-----",name)
    plt.figure(inc)
    data.reset_index(inplace=True)

    
    df_volume = data['Adj Close']

    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.suptitle(name)

    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=5, colspan=1, sharex = ax1)
    ax2.set_title('Volume')

    #date functions cause viewlimit crash due to same datetime reason as resample() issue, dont use
    #ax1.xaxis_date()
    #ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    
    try:
        candlestick2_ohlc(ax1, data['Open'], data['High'],data['Low'],data['Close'], width=.6, colorup='#00eeff', colordown='#ff0044', alpha =.4)
    except:
        print('ERROR candlestick2_ohlc failed')
        main()


    #fills volume visual with data
    ax2.fill_between(data.index, data['Volume'].values, 0)

    #add spacing between subplots
    plt.subplots_adjust(hspace=0.7)

    #formats the y axis ticker to represent dollars
    formatter = ticker.FormatStrFormatter('$%1.2f')
    ax1.yaxis.set_major_formatter(formatter)

    for tick in ax1.yaxis.get_major_ticks():
        tick.label1.set_visible(False)
        tick.label2.set_visible(True)
        #tick.label2.set_color('green')

    #sets ticker to the left side
    ax1.yaxis.tick_left()
    ax1.yaxis.set_label_position("left")
    ax1.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.4)

    #maximizes window
    #this backend is: TkAgg
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())

    return


def candlestickIt(data, inc, name, useCsv):
    tickName = name
    if useCsv == 1:
        dataFrame = pd.read_csv("CsvFolder/"+tickName+".csv", parse_dates=['Date'])
        df = dataFrame

    else:
        df = data

    increment = inc
    #matplot figure allows for multiple instances/windows to be made
    plt.figure(increment)
    plt.suptitle(tickName)
    df = data
    print(df.head())


    #creates and resamples the dataframe to show the weekly change
    #do not resample to less than 4D - bad things happen(down bars disappear)
    df_ohlc = df['Adj Close'].resample('4D').ohlc()
    df_volume = df['Adj Close'].resample('4D').sum()
    
    df_ohlc.reset_index(inplace=True)

    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)


    #create subplots to represent data
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)

    #need ax2 to match ax1 so that when zooming on one graph the other matches
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=5, colspan=1, sharex = ax1)
    
    ax2.set_title('Volume')

    #date format for x axis
    ax1.xaxis_date()
    
    #formats the y axis ticker to represent dollars
    formatter = ticker.FormatStrFormatter('$%1.2f')
    ax1.yaxis.set_major_formatter(formatter)

    for tick in ax1.yaxis.get_major_ticks():
        tick.label1.set_visible(False)
        tick.label2.set_visible(True)
        #tick.label2.set_color('green')

    #sets ticker to the left side
    ax1.yaxis.tick_left()
    ax1.yaxis.set_label_position("left")

    #Build candlestick chart
    try:
        candlestick_ohlc(ax1, df_ohlc.values, width=1.8, colorup='#00eeff', colordown='#ff0044', alpha =.4)
    except:
        print("ERROR build went wrong within candlestick method")
        main()
        
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

    #add spacing between subplots
    plt.subplots_adjust(hspace=0.7)

    ax1.grid(b=True, which='major', color='grey', linestyle='-', alpha=0.4)
    
    #maximizes window
    #this backend is: TkAgg
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    return

    

#### Beginning of Main ###
def main():
    loadFromFile = input("would you like to load from file?(Y/N):").upper()

    if(loadFromFile == "Y"):
        print("Here's a list of files in the current directory:")
        arr = os.listdir()
        print(arr)
        loadFile(input("specify filename:"))
        print('Compeleted')
        if(input("Would you like to re-run the program?(Y/N):").upper() == "Y"):
            main()
    else:
        #default graphing style
        style.use('dark_background')

        if(input("Would you like to see a small portion of the s&p500 tickers?(Y/N):").upper() == 'Y'):
            showTickList()
        #Date range to show
        print("\n--only displays data from the first day of start year to the last day of end year--")
        try:
            userStart = int(input("start year: "))
            userEnd = int(input("End Year: "))
        except:
            print('invalid data entered')
            main()

        #goes from the first day of start year to last day of end year -- plots to the widest range its has data for up to the current day
        start = datetime.datetime(userStart,1,1)
        end = datetime.datetime(userEnd,12,31)


        #stock to choose
        tick = input("type stock name here: ")
        ticker = tick.upper()
        print(ticker)

        #Gathers chosen tickers data from yahoo finance api
        try:
            dataFrame = web.DataReader(ticker, 'yahoo', start, end)
        except:
            print('!!Error!!(Make sure you entered a valid ticker)')
            main()

        print('\n' + "Heres the default data gathered for:", ticker, '\n')
        print(dataFrame.head())

        if(input("would you like this stock represented as a candlestick?(Y/N)").upper() == "Y"):
            candlestickIt(dataFrame, 1, ticker, 0)
        else:
            defaultIt(dataFrame, 1, ticker, 0)

        showPlot()

        toSave = input("would you like to add this stock to a file?(Y/N):").upper()

        if(toSave == "Y"):
            addIt(ticker, userStart, userEnd)

        if(input("Would you like to re-run the program?(Y/N):").upper() == "Y"):
            main()


def mainFromFile(tickerDict, numberCsv):
    print('\n---Loading from file---\n')
    dictMain = tickerDict
    print(dictMain.keys(), dictMain.items())
    csvBool = False
    readCsv = numberCsv

    #CSV's load alot faster, ask if user wants to load from list, using any existing csvs
    if(input("would you like to convert each stock in the file to a csv aswell?(Y/N):").upper() == "Y"):
        csvBool = True
    if(input("would you like this stock represented as a candlestick?(Y/N)").upper() == "Y"):
        #keep track of cycles to increment plt.figure() for multiple windows
        count = 0
        bar = progressbar.ProgressBar()
        
        for key in bar(dictMain.keys()):

            #pull list of values from key - should only be 2: start, end
            dictValues = dictMain[key][0::1]


            print("\n" + str(dictValues) + "\n")

            userStart = int(dictValues[0])
            userEnd = int(dictValues[1])
                    
            print('start:', userStart)
            print('end:', userEnd)

            #default graphing style
            style.use('dark_background')

            #Date range to show
            #goes from the first day of start year to last day of end year -- plots to the widest range its has data for up to the current day
            end = datetime.datetime(userEnd,12,31)
            start = datetime.datetime(userStart,1,1)
            


            #ticker to select
            tick = key
            print(tick)
            ticker = tick.upper()
            print(ticker)


            #makeRegular = 0
            #call yahoo api to fetch data on ticker unless user wants to use csvs
            if readCsv == 0:
                dataFrame = web.DataReader(ticker, 'yahoo', start, end)
                

                print('\n' + "Heres the data gathered for:", ticker, '\n')
                print(dataFrame.head())
            else:
                if os.path.exists("CsvFolder/"+ticker+".csv"):
                    dataFrame = pd.read_csv("CsvFolder/"+ticker+".csv")
                else:
                    dataFrame = web.DataReader(ticker, 'yahoo', start, end)
                    print('\n' + "Heres the data gathered for:", ticker, '\n')
                    print(dataFrame.head())

            
                print('\n' + "Heres the data gathered for:", ticker, '\n')
                print(dataFrame.head())

            #if user wants file made into csv's
            if(csvBool == True):
                makeCsv(dataFrame, ticker)

            try:
                if readCsv == 1:
                    csvCandle(dataFrame, count, ticker)
                else:
                    candlestickIt(dataFrame, count, ticker, readCsv)
            except:
                print("ERROR ohlc chart could not be created, Heres the log:", count, ticker, readCsv)
                main()
            count += 1
    else:
        #same as above for candlestick - however call defaultIt() instead
        #keep track of cycles to increment plt.figure() for multiple windows
        count = 0
        bar = progressbar.ProgressBar()
        #CSV's load alot faster, ask if user wants to load from list, using any existing csvs
        for key in bar(dictMain.keys()):

            dictValues = dictMain[key][0::1]


            print("\n" + str(dictValues) + "\n")

            userStart = int(dictValues[0])
            userEnd = int(dictValues[1])
                    
            print('start:', userStart)
            print('end:', userEnd)

            #default graphing style
            style.use('dark_background')

            #Date range to show
            end = datetime.datetime(userEnd,1,1)
            start = datetime.datetime(userStart,1,1)
            


            #stock to retrieve data on
            tick = key
            print(tick)
            ticker = tick.upper()
            print(ticker)

            if readCsv == 0:
                dataFrame = web.DataReader(ticker, 'yahoo', start, end)
                print('\n' + "Heres the data gathered for:", ticker, '\n')
                print(dataFrame.head())
            else:
                if os.path.exists("CsvFolder/"+ticker+".csv"):
                  
                    dataFrame = pd.read_csv("CsvFolder/"+ticker+".csv")
                else:
                    dataFrame = web.DataReader(ticker, 'yahoo', start, end)
                    print('\n' + "Heres the data gathered for:", ticker, '\n')
                    print(dataFrame.head())

                print('\n' + "Heres the data gathered for:", ticker, '\n')
                print(dataFrame.head())

            if(csvBool == True):
                makeCsv(dataFrame,ticker)

            print('\n' + "Here's the data gathered for:", ticker, '\n')
            print(dataFrame.head())
            try:
                defaultIt(dataFrame, count, ticker, readCsv)
            except:
                print("ERROR the Adj Close graph could not be built")
                main()
            count += 1

            
    # conditionals run fetching data and sending it to their 
    # respective functions to build the figures and windows, 
    # this final call builds and shows the scene after the prior is completed
    showPlot()
    return


#This only executes on first start up       
print('                     ~Welcome to MintyStocks~                       ')
print("""\
                                                                          ^
                                       ._ o o                            /
                                       \_`-)|_                          /
                                    ,""       \                        / 
                                  ,"  ## |   ಠ ಠ.             /\      /
                                ," ##   ,-\__    `.      /\  /  \    /
                              ,"       /     `--._;)    /  \/    \  /   
                            ,"     ## /              /\/          \/
                          ,"   ##    /              /
                                                   /

                    """)

main()