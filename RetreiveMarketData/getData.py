import pandas as pd
import datetime
import time
import os
from kite_trade import *



instrument_symbol = 'NIFTY 50'
# instrument_symbol = 'NIFTY BANK'
timeFrame = '30minute'
# -----------Initializing KiteApp---------------
# // place your enctoken here 
enctoken = "F9Hc0uIzMT45nK5hBfQW2BhpnwCXcp7H00lH+/F7LMC6oZ+5KKk+h2wAvUbwYOEVWZFYpjT65N3AFRURBOxcihIEMXIfoOxog9SZxtlJOQ81LVb1Exx57w=="
kite = KiteApp(enctoken=enctoken)

nse = kite.instruments('NSE')
nse_data = pd.DataFrame(nse)
inst_token = (nse_data[nse_data.tradingsymbol == instrument_symbol].instrument_token.values[0])

# Define start and end dates
start_date = datetime.datetime(2020, 12, 1)
end_date = datetime.datetime.now()

# Create folder to store data
folder_path = f'{instrument_symbol}_{timeFrame}_data'
os.makedirs(folder_path, exist_ok=True)

# Iterating over 3-month periods
while start_date < end_date:
    # Calculate the end date for the current 3-month period
    period_end_date = start_date + datetime.timedelta(days=3*30)

    # Fetch historical data for the current 3-month period
    nifty_50_data = pd.DataFrame(kite.historical_data(inst_token, start_date.strftime('%Y-%m-%d'), period_end_date.strftime('%Y-%m-%d'), timeFrame))

    # Save the DataFrame as a CSV file
    filename = os.path.join(folder_path, f'{instrument_symbol}_{timeFrame}_data_{start_date.strftime("%Y%m%d")}.csv')
    nifty_50_data.to_csv(filename, index=False)

    # Update start date for the next 3-month period
    start_date = period_end_date

    # Add a delay to respect API rate limits
    time.sleep(1)

# Get a list of all CSV files in the folder
file_list = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Create an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Iterate over each file and merge the data
for file in file_list:
    file_path = os.path.join(folder_path, file)
    data = pd.read_csv(file_path)
    merged_data = pd.concat([merged_data, data])

# Save the merged data as a new CSV file
merged_filename = os.path.join(folder_path, f'{instrument_symbol}_data_{timeFrame}_merged.csv')
merged_data.to_csv(merged_filename, index=False)
