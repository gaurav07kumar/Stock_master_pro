import pandas as pd
import datetime
import time
# from datetime import datetime, time
from kite_trade import *

enctoken = "pwNuREgvuzJYgJfzPiK7AQ8td1MR9Ik7J9EmJ+lzuDZ/0iq2psJulpDF1vWQdQRffQUZlZ/G07b5bkX825pntw5NwifvT5QzeKj/t82fJyx8J1/dV2Mgfg=="
kite = KiteApp(enctoken=enctoken)

instrument = 'NIFTY 50'
nse = kite.instruments('NSE')
nse_data = pd.DataFrame(nse)
nifty = (nse_data[nse_data.tradingsymbol == instrument ].instrument_token.values[0])


# // DEFINE YOUR INPUTS HERE 
tradingsymbol = 'IDEA'  # Replace with what you want to trade 
timeFrame = '10minute'
exchange = 'NSE'
quantity = 1  # Replace with the quantity you want to sell
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

def bullishEngulfing(ptr,data):
    rd = data['close'].iloc[ptr-1] < data['open'].iloc[ptr-1]
    gr = data['close'].iloc[ptr] > data['open'].iloc[ptr]
    bt = data['close'].iloc[ptr] > data['open'].iloc[ptr-1]
    temp = data['close'].iloc[ptr] > twenty_ema(ptr,data)
    return rd and gr and bt and temp 

def bearEngulfing(ptr,data):
    rd = data['close'].iloc[ptr-1] > data['open'].iloc[ptr-1]
    gr = data['close'].iloc[ptr] < data['open'].iloc[ptr]
    bt = data['close'].iloc[ptr] < data['open'].iloc[ptr-1]
    temp = data['close'].iloc[ptr] < twenty_ema(ptr,data)
    return rd and gr and bt  and temp 

def twenty_ema(ptr,data) : 
    sum = 0
    for i  in range(20):
        sum += data['close'].iloc[ptr-i]
    return sum/20.0

def getmeDate(ptr,data): 
    datetime_string = data['date'].iloc[ptr]
    datetime_obj = pd.to_datetime(datetime_string)
    return datetime_obj.date()

def getmeTime(ptr,data): 
    datetime_string = data['date'].iloc[ptr]
    datetime_obj = pd.to_datetime(datetime_string)
    return datetime_obj.time()


start_time = datetime.time(10, 15)
end_time = datetime.time(15, 0)

# //Analysing parameters
positive_trades = 0
negative_trades = 0
maxLoss = 0  
maxProfit = 0
totalProfit = 0


openPosition = False
entry = -1 
transaction_data = []
ema_9 = 0
long = False
short = False
maxLoss_stoploss = 30
trade_count = 0
prev_i = -1

while trade_count < 2 :
    from_date = datetime.datetime(2023, 7, 4)
    to_date = datetime.datetime.now()
    dd =(kite.historical_data(nifty,from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'), timeFrame))
    data = pd.DataFrame(dd)
    i = len(data)  - 1

    if i == prev_i : continue
    prev_i = i
    if openPosition :
        # current_price = float(data['close'].iloc[i])
        current_price = kite.ltp(instrument)
        today_date = getmeDate(i,data)
        if long :
            x = max(data['close'].iloc[entry] - maxLoss_stoploss ,min( data['low'].iloc[entry] , data['low'].iloc[entry-1]))
            stopLoss = current_price <= x
            if   stopLoss  or getmeTime(i,data) >= end_time: # if current close < 9 EMA
                openPosition = False
                long = False
                exit = i 
                entry_price = data['close'].iloc[entry]
                exit_price = data['close'].iloc[i]
                if stopLoss : 
                    exit_price = x
                profit_loss = exit_price - entry_price
                transaction_data.append({'Date': data['date'].iloc[entry],'Position': 'long', 'Entry': entry_price, 'Exit': exit_price,'Exit_Date': data['date'].iloc[i], 'Profit/Loss': profit_loss})
                trade_count += 1 

                totalProfit += profit_loss 
                if profit_loss<0 : 
                    negative_trades += 1
                else :
                    positive_trades += 1
                maxProfit = max(maxProfit,profit_loss)
                maxLoss = min(maxLoss,profit_loss)
                exitPosition('long')
        elif short :
            x = min(data['close'].iloc[entry] + maxLoss_stoploss ,max( data['high'].iloc[entry] , data['high'].iloc[entry-1]))
            stopLoss = current_price >= x
            if   stopLoss  or getmeTime(i,data) >= end_time: # if current close < 9 EMA
                openPosition = False
                short = False
                exit = i 
                entry_price = data['close'].iloc[entry]
                exit_price = data['close'].iloc[i]
                if stopLoss : 
                    exit_price = x

                profit_loss =  entry_price - exit_price
                transaction_data.append({'Date': data['date'].iloc[entry],'Position': 'short', 'Entry': entry_price, 'Exit': exit_price,'Exit_Date': data['date'].iloc[i], 'Profit/Loss': profit_loss})
                trade_count += 1 

                totalProfit += profit_loss 
                if profit_loss<0 : 
                    negative_trades += 1
                else :
                    positive_trades += 1
                maxProfit = max(maxProfit,profit_loss)
                maxLoss = min(maxLoss,profit_loss)
                exitPosition('short')

    else :
        if bullishEngulfing(i,data) and start_time <= getmeTime(i,data)  :
            if trade_count >= 2 :
                continue
            entry = i 
            openPosition = True
            long = True
            print('Bullish',data['date'].iloc[i])
            placeOrder('long')
        if bearEngulfing(i,data) and start_time <= getmeTime(i,data)  :
            if trade_count >= 2 :
                continue
            entry = i 
            short = True
            openPosition = True
            print('Bearish',data['date'].iloc[i])
            placeOrder('short')




# Create a DataFrame from the transaction data
transaction_data.append({'TotalTrades': positive_trades+negative_trades,'PositiveTrades': positive_trades, 'NegativeTrades': negative_trades, 'Max Profit': maxProfit,'maxLoss': maxLoss, 'total': totalProfit})
transaction_df = pd.DataFrame(transaction_data)
transaction_df.to_csv('potential_Trades.csv', index=False)

def instrument_token(data, symbol):
    return data[data.tradingsymbol == symbol].instrument_token.values[0]
