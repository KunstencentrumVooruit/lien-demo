import urllib2
import json
from urllib2 import Request, urlopen, URLError, HTTPError
import apikey

class yesplanAPIQuery2:

  def __init__(self):
    self.apikey=apikey.apikey

  # functie die query uitvoert en json object teruggeeft.
  def get_data(self, query):

    url = urllib2.Request("https://vooruit.yesplan.be/api"+query+"?api_key="+self.apikey)

    try:
      response = urllib2.urlopen(url)
      readdata = response.read()
      jsonstring=json.loads(readdata)

    except HTTPError as e:
      print e.code


    except URLError as e:
      print 'Reason: ', e.reason

    return jsonstring

  def get_next_data(self, query):

    url = urllib2.Request(query+"&api_key="+self.apikey)

    try:
      response = urllib2.urlopen(url)
      readdata = response.read()
      jsonstring=json.loads(readdata)

    except HTTPError as e:
      print e.code


    except URLError as e:
      print 'Reason: ', e.reason

    return jsonstring

  # recursief zoeken
  def traverse(path):

    i=0
    for id in path:

      if 'children' in path[i]:
        if path[i]["resource"]["name"][:3] == "SET":
          path2=path[i]['children']
          #print path2
          traverse(path2)
    i=i+1
