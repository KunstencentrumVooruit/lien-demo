import json
import gspread
import apikey
from oauth2client.client import SignedJwtAssertionCredentials
from yesplanAPIQuery2 import yesplanAPIQuery2
import locale
import datetime
import datetime
from dateutil import parser

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
  # data = query.get_data("/event/5692949505-1416475956")
  data = query.get_data("/events/name%3Ademo")

  #CONCERTZAAL
  #BALZAAL
  #THEATERZAAL

  i=0

  # voorstellingen = []
  # wut = []
  samen = []

  for w in data["data"]:
    id=data["data"][i]["id"]
    lokatie = data['data'][i]['locations'][0]['name']
    aanvangsuur = data['data'][i]['starttime']

    # aanvangsuurr = datetime.strptime(aanvangsuur, '%Y-%m-%dT%H:%M:%S.%fZ')
    aanvangsuurr = parser.parse(aanvangsuur)



    # aanvangsuur=data["data"][i]["defaultschedulestarttime"]

    samen.append(lokatie)
    if aanvangsuur > date.today()-datetime.timedelta(days=7):
      samen.append(aanvangsuurr)

    # wut.append(aanvangsuur)
    i=i+1

  return samen


def exportToSheet(query, worksheet, samen):

  # worksheet.update_cell(5, 5, naam)
  teller = 0

  for sam in samen:
    print sam
    # print wut
    # worksheet.update_cell(1, teller, voorstelling[teller])

  teller = teller + 1


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


