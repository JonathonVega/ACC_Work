import openpyxl
import time

print("Hello, World!")

time.sleep(2)

wbMain = openpyxl.load_workbook('WebsiteToText\SCArticles.xlsx')

print(wbMain.get_sheet_names())
sheetMain = wbMain.get_sheet_by_name('SCArticles')
sheetMain['H1'] = "FirstPageNo"
wbMain.save('SCArticles&JACCJournals0.xlsx')

wbMain = openpyxl.load_workbook('SCArticles&JACCJournals0.xlsx')
sheetMain = wbMain.get_sheet_by_name('SCArticles')

wbSC = openpyxl.load_workbook('WebsiteToText\XJACCJournalData.xlsx')
sheetSC = wbSC.get_sheet_by_name('JACCJournalData')
print(sheetSC['A1'].value)
print('ok')
for row in range(2, 73550):
    articleDOI = sheetMain.cell(row = row, column = 2).value
    print(articleDOI)
    for jrow in range(2, 25700):
        jDOI = sheetSC.cell(row = jrow, column = 1).value
        print(jDOI)
        if(articleDOI == jDOI):
            sheetMain['H' + str(row)] = sheetSC['D' + str(jrow)].value
            print('FOUND!!!')
            break
        else:
            continue
wbMain.save('SCArticles&JACCJournals0.xlsx')

time.sleep(100)
