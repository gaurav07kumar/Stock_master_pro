from kite_trade import *
enctoken = "pXwHHlApvgS1X2guyiCU5i1uu8ywV9tBkUT9kgn86PHRlx8dZJYO7RSRiWqRpHCXn+bkQm9RQOxLQrCvjFd/SJ8qMcEX+mRZKPmyuJTbpLR+yVpePqVWjA=="
kite = KiteApp(enctoken=enctoken)

# ************************************
import pandas as pd
import datetime
import time

# // DEFINE YOUR INPUTS HERE 
exchange = 'NSE'
tradingsymbol = 'IDEA'  # Replace with your instrument symbol
quantity = 1  # Replace with your ordre quantity
order_type = kite.ORDER_TYPE_MARKET
product = kite.PRODUCT_MIS

def placeOrder(positionType) :
    if positionType == 'long' :
        transaction_type = kite.TRANSACTION_TYPE_BUY
    elif positionType == 'short' :
        transaction_type = kite.TRANSACTION_TYPE_SELL
    
    orderis = kite.place_order(variety=kite.VARIETY_REGULAR,
                            exchange=kite.EXCHANGE_NSE,
                            tradingsymbol=tradingsymbol,
                            transaction_type=transaction_type,
                            quantity=quantity,
                            product=product,
                            order_type=order_type)
    print(orderis)

def exitPosition(positionType) :
    if positionType == 'short' :
        transaction_type = kite.TRANSACTION_TYPE_BUY
    elif positionType == 'long' :
        transaction_type = kite.TRANSACTION_TYPE_SELL
    
    orderis = kite.place_order(variety=kite.VARIETY_REGULAR,
                            exchange=kite.EXCHANGE_NSE,
                            tradingsymbol=tradingsymbol,
                            transaction_type=transaction_type,
                            quantity=quantity,
                            product=product,
                            order_type=order_type)
    print(orderis)


nse = kite.instruments('NFO')

nse_data = pd.DataFrame(nse)
inst_token = (nse_data[nse_data.tradingsymbol == 'NIFTY23JUL19400PE'].instrument_token.values[0])

from_date = datetime.datetime(2023, 7, 3)
to_date = datetime.datetime.now()

print(kite.historical_data(inst_token,from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'), '10minute'))

# // YOU CAN PLACE YOUR ORDER HERE 
placeOrder('long')
placeOrder('short')

#  EXIT USING THESE 
exitPosition('long')
exitPosition('short')













































































# import pandas as pd
# import csv
# nse = kite.instruments('NSE') #replace 'NSE' with 'BSE' for BSE data
# nse_data = pd.DataFrame(nse)

# inst_token = (nse_data[nse_data.tradingsymbol == 'NIFTY 50'].instrument_token.values[0])

# nifty_50_data = pd.DataFrame(kite.historical_data(inst_token, '2021-01-01' , '2021-04-28', '10minute'))
# print(nifty_50_data)
# nifty_50_data.to_csv('nifty_50_data_big.csv', index=False)


# def instrument_token(data, symbol):
#     """
#     This function will return the token number of the instrument from data
#     """
#     return data[data.tradingsymbol == symbol].instrument_token.values[0]

# def historical_data(symbol, from_date, to_date, interval):
#     """
#     This function will return historical data of the instrument for specific period of days for specific interval
#     """
    
#     df = pd.DataFrame()   
#     int_token = instrument_token(nse_data, symbol)  #the function we defined above which will return token no. of instrument
    
#     to_date   = pd.Timestamp(to_date)
#     from_date = pd.Timestamp(from_date)

#     while True:
#         if from_date >= (to_date - dt.timedelta(60)):                     #if from_date is within the 60 days limit
#             df = df.append(pd.DataFrame(kite.historical_data(int_token, from_date, to_date, interval)))
#             break
            
#         else:                                                            #if from_date has more than 60 days limit
#             to_date_new = from_date + dt.timedelta(60)
            
#             df = df.append(pd.DataFrame(kite.historical_data(int_token, from_date, to_date_new, interval)))
            
#             #to_date = from_date.date() + dt.timedelta(60)
#             from_date = to_date_new
            
#     return df


# NIFTY_50_2023 = historical_data('NIFTY 50', '01-05-2023', '28-03-2023', 'minute')
# print(NIFTY_50_2023)