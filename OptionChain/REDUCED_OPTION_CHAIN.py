import pandas as pd
import xlwings as xw
import pandas as pd
import datetime
import time as t
import csv
from datetime import datetime, time
from kite_trade import *

enctoken = "t2WbcAWRnpWauQ6ZCOe80gF5nSStOVOFa0hLaXUg6H3EwT6p2idFw3QGBRaK/czyobFKZXTksTAxY09r2An+jb0jcFm8Bw2PeoRQHQVKtkz0AunTgewrWg=="
kite = KiteApp(enctoken=enctoken)

expiry = '2023-08-17'
expiry_date = datetime.strptime(expiry, '%Y-%m-%d').date()
d = kite.instruments('NFO')
dd = pd.DataFrame(d)

# final_dd = dd[dd['tradingsymbol'].str.startswith('NIFTY') & (dd['expiry'] == expiry_date) & (dd['strike'] > 18500) & (dd['strike'] < 19000) ]
final_dd = dd[dd['tradingsymbol'].str.startswith('NIFTY') & (dd['expiry'] == expiry_date)  ]
final_dd = final_dd.sort_values(by='instrument_type')

ce = dd[dd['tradingsymbol'].str.startswith('NIFTY') & (dd['expiry'] == expiry_date)  & (dd['instrument_type'] == 'CE')  ]

pe = dd[dd['tradingsymbol'].str.startswith('NIFTY') & (dd['expiry'] == expiry_date)  & (dd['instrument_type'] == 'PE')  ]

xlsx_file = 'reduced_option_chain.xlsx'
sheet_name = 'reduced option chain'

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
# Create a new Excel workbook
# wb = xw.Book()

# sheet_name = 'Sheet1'
# sheet_names = wb.sheets.names
# if sheet_name in sheet_names:
#     sheet_name += "_new"
# sheet = wb.sheets.add(sheet_name)
call = wb.sheets('call')
put = wb.sheets('put')
# put = wb.sheets.add('call')
call.range('A1').value = ce
put.range('A1').value = pe

df = final_dd
nifty = '10930434'


while True:
    va = pd.DataFrame(kite.ltp(nifty))
    atm = (round(va[nifty]['last_price'],-2))
    print(atm)
    df = dd[dd['tradingsymbol'].str.startswith('NIFTY') & (dd['expiry'] == expiry_date) & (dd['strike'] > atm-1000) & (dd['strike'] < atm+1000) ]
    call = df[ (df['strike'] <= atm )& (df['instrument_type'] == 'CE')]
    put = df[  (df['strike'] >= atm ) & (df['instrument_type'] == 'PE')]
    df = pd.concat([call, put], ignore_index=True)
    df = df.sort_values(by='instrument_type')
    instrument_tokens = df['instrument_token'].tolist()

    quote_ltp = kite.ltp(instrument_tokens)
    last_prices = [value['last_price'] for value in quote_ltp.values()]
    df['last_price'] = last_prices

    sheet.range('A1').value = df
    print(last_prices)
    print('working')
    wb.save()

