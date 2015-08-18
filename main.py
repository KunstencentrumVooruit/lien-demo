import json
import gspread
import apikey
from oauth2client.client import SignedJwtAssertionCredentials
from yesplanAPIQuery2 import yesplanAPIQuery2
import locale
import datetime


def getDate(delta):
  today = datetime.date.today() + datetime.timedelta(days=delta)
  date = str(today.day)+"-"+str(today.month)+"-"+str(today.year)
  return date

class googleSheet():
  def __init__(self, sheetName):
    self.json_key = json.load(open('Vooruit-b6b35f5c38b1.json'))
    self.scope = ['https://spreadsheets.google.com/feeds']
    self.credentials = SignedJwtAssertionCredentials(self.json_key['client_email'], self.json_key['private_key'], self.scope)
    self.gc = gspread.authorize(self.credentials)
    self.wks = self.gc.open(sheetName)


def getActivity(query):
  data = query.get_data("/event/5692949505-1416475956")

  naam = data['name']

  return naam


def exportToSheet(query, worksheet, naam):

  worksheet.update_cell(1, 2, naam)


def main():
  gSheet = googleSheet('test')

  query = yesplanAPIQuery2()

  worksheet = gSheet.wks.get_worksheet(0)

  cell_list = worksheet.range('A4:B30')
  for cell in cell_list:
    cell.value=''

  worksheet.update_cells(cell_list)
  naam = getActivity(query)
  exportToSheet(query, worksheet, naam)






main()


