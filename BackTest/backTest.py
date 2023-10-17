import pandas as pd
import ta
import csv
from datetime import datetime, time

data = pd.read_csv('Data.csv') # RELIANCE_data_10min_merged.csv

# // ptr refers to pointer
def bullishEngulfing(ptr):
    rd = data['close'].iloc[ptr-1] < data['open'].iloc[ptr-1]
    gr = data['close'].iloc[ptr] > data['open'].iloc[ptr]
    bt = data['close'].iloc[ptr] > data['open'].iloc[ptr-1]
    xt = data['open'].iloc[ptr] < data['close'].iloc[ptr-1]
    # atroo = atr(ptr,1) > atr(ptr,80)
    temp = data['close'].iloc[ptr] > twenty_ema(ptr)
    return rd and gr and bt and  xt and temp

def bearEngulfing(ptr):
    rd = data['close'].iloc[ptr-1] > data['open'].iloc[ptr-1]
    gr = data['close'].iloc[ptr] < data['open'].iloc[ptr]
    bt = data['close'].iloc[ptr] < data['open'].iloc[ptr-1]
    xt = data['open'].iloc[ptr] > data['close'].iloc[ptr-1]
    # atroo = atr(ptr,1) > atr(ptr,80)
    temp = data['close'].iloc[ptr] < twenty_ema(ptr)
    return rd and gr and bt and xt and temp


def nine_ema(ptr) : 
    sum = 0
    for i  in range(9):
        sum += data['close'].iloc[ptr-i]
    return sum/9.0

def twenty_ema(ptr) : 
    sum = 0
    for i  in range(20):
        sum += data['close'].iloc[ptr-i]
    return sum/20.0

def atr(ptr, period):
    sum_tr = 0
    for i in range(period):
        high = data['high'].iloc[ptr-i]
        low = data['low'].iloc[ptr-i]
        close = data['close'].iloc[ptr-i-1]
        tr = max(high - low, abs(high - close), abs(low - close))
        sum_tr += tr
    return sum_tr / period

def getmeDate(ptr): 
    datetime_string = data['date'].iloc[ptr]
    datetime_obj = pd.to_datetime(datetime_string)
    return datetime_obj.date()

def getmeTime(ptr): 
    datetime_string = data['date'].iloc[ptr]
    datetime_obj = pd.to_datetime(datetime_string)
    return datetime_obj.time()

start_time = time(10, 15)
end_time = time(15, 0)


positive_trades = 0
negative_trades = 0
maxLoss = 0  
maxProfit = 0
totalProfit = 0

# Trading Parameters
openPosition = False
entry = -1 
transaction_data = []
ema_9 = 0
long = False
short = False
maxLoss_stoploss = 5

trade_count = 0
today_date = getmeDate(0)

for i in range(len(data)):
      
    if i < 20  : continue
    if getmeDate(i) != today_date :
        trade_count = 0

    if openPosition :
        current_close = float(data['close'].iloc[i])
        today_date = getmeDate(i)
        if long :
            x = max(data['close'].iloc[entry] - maxLoss_stoploss ,min( data['low'].iloc[entry] , data['low'].iloc[entry-1]))
            stopLoss = current_close <= x
            # stopLoss = current_close <= min(data['low'].iloc[entry],data['low'].iloc[entry-1])
            if   stopLoss  or getmeTime(i) >= end_time: # if current close < 9 EMA
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
                # positive_trades += 1
                if profit_loss<0 : 
                    negative_trades += 1
                else :
                    positive_trades += 1
                maxProfit = max(maxProfit,profit_loss)
                maxLoss = min(maxLoss,profit_loss)
        elif short :
            # stopLoss = current_close >= max(data['high'].iloc[entry],data['high'].iloc[entry-1])
            x = min(data['close'].iloc[entry] + maxLoss_stoploss ,max( data['high'].iloc[entry] , data['high'].iloc[entry-1]))
            stopLoss = current_close >= x
            if   stopLoss  or getmeTime(i) >= end_time: # if current close < 9 EMA
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

    else :
        if bullishEngulfing(i) and start_time <= getmeTime(i)  :
            if trade_count >= 2 :
                continue
            entry = i 
            openPosition = True
            long = True
            print('Bullish',data['date'].iloc[i])
        if bearEngulfing(i) and start_time <= getmeTime(i)  :
            if trade_count >= 2 :
                continue
            entry = i 
            short = True
            openPosition = True
            print('Bearish',data['date'].iloc[i])

transaction_data.append({'TotalTrades': positive_trades+negative_trades,'PositiveTrades': positive_trades, 'NegativeTrades': negative_trades, 'Max Profit': maxProfit,'maxLoss': maxLoss, 'total': totalProfit})
                   
# Create a DataFrame from the transaction data
transaction_df = pd.DataFrame(transaction_data)

# Save the transaction data as a new CSV file
transaction_df.to_csv('TotalTrades.csv', index=False)

