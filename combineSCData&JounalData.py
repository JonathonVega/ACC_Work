import openpyxl
import time

print("Hello, World!")

wbMain = openpyxl.load_workbook('WebsiteToText\SCArticles&JACCJournals.xlsx')

print(type(wbMain))
print(wbMain.get_sheet_names())
sheetMain = wbMain.get_sheet_by_name('Sheet1')
#sheetMain['A1'] = "Hello"
wbMain.save('SCArticles&JACCJournals0.xlsx')

wbSC = openpyxl.load_workbook('WebsiteToText\SCArticles.xlsx')
sheetSC = wbSC.get_sheet_by_name('SCArticles')
print(sheetSC['A1'].value)
print('ok')
for row in range(0, 73550):



time.sleep(100)
