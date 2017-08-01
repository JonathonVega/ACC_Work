import openpyxl
import time
import requests
import csv
from bs4 import BeautifulSoup

suppSites = ['http://www.onlinejacc.org/content/meeting-abstract-supplements', 'http://www.interventions.onlinejacc.org/content/meeting-abstract-supplements']

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
    #print(scienceDirectLinks)
    return scienceDirectLinks

# example: http://www.sciencedirect.com/science/journal/07351097/69/11/supp/S
SDLinksList = getScienceDirectLinks()
print(SDLinksList)
print("cool")
wbOriginal = openpyxl.load_workbook('SCArticlesAbstractsOnly.xlsx')

print(wbOriginal.get_sheet_names())
sheetOriginal = wbOriginal.get_sheet_by_name('SCArticles')

numOfRows = sheetOriginal.max_row
numOfColumns = sheetOriginal.max_column
print(numOfColumns)

filepath = 'C:\\Users\\jvega\\Documents\\PythonScripts\\SCAAONew.xlsx'
wbNew = openpyxl.Workbook()
wbNew.save(filepath)
print('We done?')

#sheetNew = wbNew.get_sheet_by_name('Sheet')
wbNew = openpyxl.load_workbook('SCAAONew.xlsx')
sheetNew = wbNew.get_sheet_by_name('Sheet')

for column in range(1, numOfColumns + 1):
    sheetNew.cell(row=1, column=column).value = sheetOriginal.cell(row=1, column=column).value

wbNew.save('SCAAONew.xlsx')







time.sleep(10)
