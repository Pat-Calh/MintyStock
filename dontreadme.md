#Packages for install
   
    py -m pip install matplotlib
    py -m pip install mplfinance
    --> allows for new way to generate candlestick -> mpl_finance is unsupported and no longer works
    py -m pip install wheel
    -->allows for more features from mplfinance
    py -m pip install pandas
    ---> gives numpy dependency
    py -m pip install pandas-datareader
    py -m pip install colorama
    ---> allows colored words in the terminal :) -> doesnt work in python terminal :(
    py -m pip install progressbar

#issue notes:
    loading multiple windows:
    ---> got multiple windows to load however not at the same time, only when you close one does the other open????!: SOLVED
        ---> built a show function that builds the window after all the frames have been loaded and plotted

    the fill area in between on candlestick is having issues - should show the dates instead: SOLVED
    ---> why does the currency format to the right side instead of left on candlestick charts?: SOLVED

    defaultIt() method and mainV2() not loading multiple windows properly: 
    ---> loads 2 windows at same time what the heck is going on, closing the one with data allows function to cycle loading the next ticker - so its functional just ugly and not ideal
		---> SOLVED


    ISSUE:

    csv candlestick:
    cant run the resample() function on dataframes built from csv, how to workaround?:SOLVED
    ----> built a new function that uses candlestick2_ohlc instead allowing to pass in everything without resample() which was causing the original problem
        -----> I cannot get the datetime to format right for candlestick2_ohlc so its just integers of the index, volume also isnt showing properly since I cant use resample() and run sum() on it.


