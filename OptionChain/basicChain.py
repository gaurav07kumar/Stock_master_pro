import pandas as pd
# import xlsxwriter

import xlwings as xw
import pandas as pd
import datetime
import time as t
import csv
from datetime import datetime, time
from kite_trade import *

enctoken = "RuRSUMKjZ+TE3LTrS5eJWngudSCiTsTLZkKDKdrrsm68DfOY6VEVAifWl14BxEMhUQiMlACWF2u1VLpFZy/gS3IjufqLUdKGwNjdc4aFs0TyfpfXN79Exg=="
kite = KiteApp(enctoken=enctoken)

expiry = '2023-08-17'
expiry_date = datetime.strptime(expiry, '%Y-%m-%d').date()
d = kite.instruments('NFO')
dd = pd.DataFrame(d)
# final_dd = dd[dd['tradingsymbol'].str.startswith('NIFTY') & (dd['expiry'] == expiry_date) & (dd['strike'] > 18500) & (dd['strike'] < 19000) ]
final_dd = dd[dd['tradingsymbol'].str.startswith('NIFTY') & (dd['expiry'] == expiry_date)  ]

print(dd)


# ///////////////////////////////////////////////////////////


wb = xw.Book('F.xlsx')
wb = xw.Book('newF.xlsx')
sheet_name = 'Final_DD'
sheet = wb.sheets(sheet_name)
# sheet = wb.sheets.add(sheet_name)

instrument_tokens = final_dd['instrument_token'].tolist()
# Create a new Excel workbook
# wb = xw.Book()

# sheet_name = 'Sheet1'
# sheet_names = wb.sheets.names
# if sheet_name in sheet_names:
#     sheet_name += "_new"
# sheet = wb.sheets.add(sheet_name)

sheet.range('A1').value = final_dd
df = final_dd
while True:
    quote_ltp = kite.ltp(instrument_tokens)
    last_prices = [value['last_price'] for value in quote_ltp.values()]
    df['last_price'] = last_prices
    sheet.range('A1').value = df
    wb.save()

    print(last_prices)
    print('working')
    t.sleep(1)


