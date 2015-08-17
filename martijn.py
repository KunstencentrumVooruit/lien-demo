import json
import gspread
import datetime
from oauth2client.client import SignedJwtAssertionCredentials
from yesplanAPIQuery import yesplanAPIQuery
import locale

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

