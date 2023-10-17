import xlwings as xw
import pandas as pd
import datetime
import time as t
import csv
from datetime import datetime, time
from kite_trade import *

enctoken = "RuRSUMKjZ+TE3LTrS5eJWngudSCiTsTLZkKDKdrrsm68DfOY6VEVAifWl14BxEMhUQiMlACWF2u1VLpFZy/gS3IjufqLUdKGwNjdc4aFs0TyfpfXN79Exg=="
kite = KiteApp(enctoken=enctoken)

expiry = '2023-07-27'
expiry_date = datetime.strptime(expiry, '%Y-%m-%d').date()
d = kite.instruments('NFO')
dd = pd.DataFrame(d)
# final_dd = dd[dd['tradingsymbol'].str.startswith('NIFTY') & (dd['expiry'] == expiry_date) & (dd['strike'] > 18500) & (dd['strike'] < 19000) ]
final_dd = dd[dd['tradingsymbol'].str.startswith('NIFTY') & (dd['expiry'] == expiry_date)  ]

print(dd)

xlsx_file = 'OC.xlsx'
sheet_name = 'option chain'

if not os.path.exists(xlsx_file):
    wb = xw.Book()
    wb.save(xlsx_file)
else:
    wb = xw.Book(xlsx_file)

# Check if the sheet exists
if sheet_name not in wb.sheets:
    wb.sheets.add(sheet_name)

# Access the sheet
sheet = wb.sheets[sheet_name]

instrument_tokens = final_dd['instrument_token'].tolist()


sheet.range('A1').value = final_dd
df = final_dd
while True:
    quote_ltp = kite.ltp(instrument_tokens)
    print(quote_ltp)
    last_prices = [value['last_price'] for value in quote_ltp.values()]
    df['last_price'] = last_prices
    sheet.range('A1').value = df
    wb.save()
    print(last_prices)
    t.sleep(1)


