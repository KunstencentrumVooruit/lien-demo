import json
import gspread
import apikey
from oauth2client.client import SignedJwtAssertionCredentials
from yesplanAPIQuery2 import yesplanAPIQuery2
import locale
import datetime
import datetime
from dateutil import parser
import js2py

global_teller = 1

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
  data = query.get_data("/events/event%3Aprofile%3A%22demo(c)%22%20event%3Adate%3A%23next50days%20(event%3Alocation%3Aconcertzaal%20%2B%20event%3Alocation%3Atheaterzaal%20%2B%20event%3Alocation%3Abalzaal%20%2B%20event%3Alocation%3Acafe)")
  i=0
  samen = {}

  for w in data["data"]:
    ide=data["data"][i]["id"]
    lokatie = data['data'][i]['locations'][0]['name']
    aanvangsuur = data['data'][i]['starttime']
    artiest = data['data'][i]['name']
    status = data['data'][i]['status']['name']

    samen[aanvangsuur] = [lokatie, artiest, status, ide]

    i=i+1

  return samen



def exportToSheet(query, worksheet, samen):

  cellOffset = 2
  global global_teller

  for key in sorted(samen):

    aanvangsuur = key
    lokatie = samen[key][0]
    artiest = samen[key][1]
    status = samen[key][2]
    ide = samen[key][3]

    #string van maken
    aanvangsuur = str(aanvangsuur)
    #Heel de GMT boel eraf cutten
    aanvangsuur = aanvangsuur[:-9]
    #De T eruit halen en vervangen door spatie
    aanvangsuur = aanvangsuur.replace("T", " ")

    #Positioning
    if lokatie == "CONCERTZAAL":
      worksheet.update_cell(cellOffset, 1, aanvangsuur)
      worksheet.update_cell(cellOffset, 3, artiest)
      worksheet.update_cell(cellOffset, 4, status)
      worksheet.update_cell(cellOffset, 13, ide)
      cellOffset=cellOffset+1
      global_teller += 1

    if lokatie == "BALZAAL":
      worksheet.update_cell(cellOffset, 5, aanvangsuur)
      worksheet.update_cell(cellOffset, 7, artiest)
      worksheet.update_cell(cellOffset, 8, status)
      worksheet.update_cell(cellOffset, 13, ide)
      cellOffset=cellOffset+1
      global_teller += 1

    if lokatie == "THEATERZAAL":
      worksheet.update_cell(cellOffset, 9, aanvangsuur)
      worksheet.update_cell(cellOffset, 11, artiest)
      worksheet.update_cell(cellOffset, 12, status)
      worksheet.update_cell(cellOffset, 13, ide)
      cellOffset=cellOffset+1
      global_teller += 1

  #Make the headers
  worksheet.update_cell(1,1, "CONCERTZAAL")
  worksheet.update_cell(1,2, "Opmerking")
  worksheet.update_cell(1,3, "Artist")
  worksheet.update_cell(1,4, "Status")

  worksheet.update_cell(1,5, "BALZAAL")
  worksheet.update_cell(1,6, "Opmerking")
  worksheet.update_cell(1,7, "Artist")
  worksheet.update_cell(1,8, "Status")

  worksheet.update_cell(1,9, "THEATERZAAL")
  worksheet.update_cell(1,10, "Opmerking")
  worksheet.update_cell(1,11, "Artist")
  worksheet.update_cell(1,12, "Status")
  worksheet.update_cell(1,13, "Event ID")


def main():
  #Select sheet
  gSheet = googleSheet('test')

  #Select query
  query = yesplanAPIQuery2()

  #Select worksheet of above assigned sheet
  worksheet = gSheet.wks.get_worksheet(0)

  #Store all comments
  amountofrows = worksheet.row_count
  all_ids = worksheet.col_values(13)
  concertzaal_comments = worksheet.col_values(2)
  balzaal_comments = worksheet.col_values(6)
  theaterzaal_comments = worksheet.col_values(10)

  # print all_ids
  # print concertzaal_comments
  # print balzaal_comments
  # print theaterzaal_comments

  savecomments = {}
  tellen = 0
  lengte = len(all_ids)

  #Here we pair the correct comments to the correct IDs
  for _ in range(lengte):
    if concertzaal_comments[tellen] != None:
      savecomments[all_ids[tellen]] = [concertzaal_comments[tellen]]
      tellen += 1
    elif balzaal_comments[tellen] != None:
      savecomments[all_ids[tellen]] = [balzaal_comments[tellen]]
      tellen += 1
    elif theaterzaal_comments[tellen] != None:
      savecomments[all_ids[tellen]] = [theaterzaal_comments[tellen]]
      tellen += 1
    else:
      tellen += 1

  #clearing  worksheet because else it will keep the old comments on wrong places
  cells = worksheet.range('A1:N'+str(amountofrows))
  for cell in cells:
      cell.value=''
  worksheet.update_cells(cells)

  #Get activities
  naam = getActivity(query)
  #Post activities
  exportToSheet(query, worksheet, naam)

  #Set lenght of sheet, this way we can resize it correctly and when we get the comments out
  #we wont have to loop over hundreds of empty cells.
  amountofrows = worksheet.row_count
  worksheet.resize(global_teller)
  #Add another row because else the comment arrays wont have the same length
  #and then I wont be able to match  them to ID
  endrow = ["Do not remove ", "Do not remove", "Do not remove", "Do not remove", "Do not remove", "Do not remove", "Do not remove", "Do not remove", "Do not remove", "Do not remove", "Do not remove", "Do not remove", "Do not remove", "Do not remove"]
  worksheet.append_row(endrow)

  # Here we check where the comment has to be placed plus actually place them.
  for key in savecomments:

    comment = savecomments[key][0]
    #I have to do try/except because when you remove an event that had a comment
    #it will try to find and throw exception that the corresponding ID
    #is not in the new list grabbed from API
    try:
      idplaats = worksheet.find(key)
    except Exception:
      continue
        #Checking where the comment should be placed.
    if worksheet.cell(idplaats.row, 1).value != '' and idplaats != "No":
      worksheet.update_cell(idplaats.row, 2, comment)
    elif worksheet.cell(idplaats.row, 5).value != '' and idplaats != "No":
      worksheet.update_cell(idplaats.row, 6, comment)
    elif worksheet.cell(idplaats.row, 9).value != '' and idplaats != "No":
      worksheet.update_cell(idplaats.row, 10, comment)

main()


