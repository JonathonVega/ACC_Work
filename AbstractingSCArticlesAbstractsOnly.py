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

filepath = 'C:\\Users\\jvega\\Documents\\PythonScripts\\SCAAONew.xlsx'
wbNew = openpyxl.Workbook()
wbNew.save(filepath)

wbNew = openpyxl.load_workbook('SCAAONew.xlsx')
sheetNew = wbNew.get_sheet_by_name('Sheet')

for column in range(1, numOfColumns + 1):
    sheetNew.cell(row=1, column=column).value = sheetOriginal.cell(row=1, column=column).value

wbNew.save('SCAAONew.xlsx')

for link in SDLinksList:
    VI = link[link.index('/journal/') + 18: link.index('/supp')]
    volume = VI[:VI.index('/')]
    issue = VI[VI.index('/') + 1:]
    print('Volume is:' + volume + '.')
    print('Issue is:' + issue + '.')
    for originalRow in range(2,sheetOriginal.max_row):
        if(str(sheetOriginal.cell(row=originalRow, column=5).value) == volume and str(sheetOriginal.cell(row=originalRow, column=6).value) == issue):
            nextNewRow = sheetNew.max_row + 1
            print('FOUND ONE!!!')
            for column in range(1,8):
                if(column == 7):
                    sheetNew.cell(row=nextNewRow, column=column).value = '=CONCATENATE({},"-",{})'.format(str(sheetOriginal.cell(row=originalRow, column=5).value),str(sheetOriginal.cell(row=originalRow, column=6).value))
                    wbNew.save('SCAAONew.xlsx')
                else:
                    sheetNew.cell(row=nextNewRow, column=column).value = sheetOriginal.cell(row=originalRow, column=column).value
                    wbNew.save('SCAAONew.xlsx')

wbNew.save('SCAAONew.xlsx')
print('We done?')

time.sleep(10)
