#!/usr/bin/python

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
		self.json_key = json.load(open('API Project-49416146b827.json'))
		self.scope = ['https://spreadsheets.google.com/feeds']
		self.credentials = SignedJwtAssertionCredentials(self.json_key['client_email'], self.json_key['private_key'], self.scope)
		self.gc = gspread.authorize(self.credentials)
		self.wks = self.gc.open(sheetName)

def getActiviteiten(query,date):
	# GET /EVENT/date: event:ookdagklapper


	data = query.get_data("/events/date%3A%20"+date+"%20event%3Aookdagklapper%3A%22Ook%20op%20dagklapper%22")
	i=0
	# http://stackoverflow.com/questions/21416460/typeerror-unicode-object-does-not-support-item-assignment-in-dictionaries
	# prefix 'global' is niet nodig: zie http://stackoverflow.com/questions/14081308/why-is-the-global-keyword-not-required-in-this-case
	# maak een DICT van {'aanvangsuur', [id, lokatie]}
	voorstellingen={}
	for w in data["data"]:
			
			id=data["data"][i]["id"]
			lokatie = data['data'][i]['locations'][0]['name']
			aanvangsuur=data["data"][i]["defaultschedulestarttime"]
			voorstellingen[aanvangsuur]=[id,lokatie]
						
			i=i+1
	
	return voorstellingen

def exportToSheet(query,worksheet,voorstellingen,date):

	# TOON DATUM BOVENAAN
	worksheet.update_cell(1, 2, date)
	cellOffset=3
	for key in sorted(voorstellingen):
		#print "%s: %s" % (key, voorstellingen[key])
		# GET /EVENT/$ID/CUSTOMDATA
		customdata = query.get_data("/event/"+voorstellingen[key][0]+"/customdata")
		# UITVOERDER
		uitvoerder=customdata['groups'][2]['children'][0]['children'][0]['value'];
		# VOORSTELLING
		voorstelling=customdata['groups'][2]['children'][0]['children'][2]['value'];
		# LOKATIE
		lokatie=voorstellingen[key][1]
		# AANVANGSUUR
		aanvangsuur=key
		# EERSTE KOLOM: UUR
		worksheet.update_cell(cellOffset+2, 1, aanvangsuur)
		# DAARONDER LOKATIE
		worksheet.update_cell(cellOffset+3, 1, lokatie)
		# TWEEDE KOLOM: UITVOERDER
		worksheet.update_cell(cellOffset+2, 2, uitvoerder)
		# DAARONDER VOORSTELLING
		worksheet.update_cell(cellOffset+3, 2, voorstelling)

		cellOffset=cellOffset+2

def main():
	
	# NEW GOOGLESHEET OBJECT
	gSheet = googleSheet('dagklapper')
	

	# NEW YPAPIQ OBJECT
	query = yesplanAPIQuery()
	i=0
	for days in range (0,3):
		print "Fetching & exporting data for " + getDate(i)
		worksheet = gSheet.wks.get_worksheet(i)

		# Cleanup: Select a range, set value & update
		cell_list = worksheet.range('A4:B30')
		for cell in cell_list:
			cell.value=''
		worksheet.update_cells(cell_list)
		voorstellingen = getActiviteiten(query, getDate(i))
		exportToSheet(query, worksheet, voorstellingen, getDate(i))
		i=i+1
	

	

main()





