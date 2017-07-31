import openpyxl
import time
import requests
import csv
from bs4 import BeautifulSoup

suppSites = ['http://www.onlinejacc.org/content/meeting-abstract-supplements', 'http://www.interventions.onlinejacc.org/content/meeting-abstract-supplements']

print('Hello, World!')

def getScienceDirectLinks():
    scienceDirectLinks = []
    for site in suppSites:
        r = requests.get(site)
        archiveSoup = BeautifulSoup(r.text, 'lxml')
        print(archiveSoup)
        for links in archiveSoup.find_all('a', href=True):
            print(links)
            if('www.sciencedirect.com' in links.get('href')):
                scienceDirectLinks.append(links.get('href'))
                #print(links.get('href'))
    print(scienceDirectLinks)


getScienceDirectLinks()
time.sleep(100)

#wbOriginal = openpyxl.load_workbook('SCArticlesAbstractsOnly')

#print(wbOriginal.get_sheet_names())
#sheetOriginal = wbOriginial.get_sheet_by_name('SCArticles')
#sheetOriginal[]
