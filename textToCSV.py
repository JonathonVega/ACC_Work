import time
from os import listdir
from os import walk
import csv

#files = walk("C:\\Users\\jvega\\Documents\\JACCJournalsData\\WebsiteToText\\JACC1983")

allTextFilesList = []

metadataToDownload = ['\"citation_doi\"', '\"citation_volume\"', '\"citation_issue\"', '\"citation_firstpage\"']


journal = 'BTS'
with open((journal + 'JournalData.csv'), 'w', encoding='utf-8', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerow(metadataToDownload)
    for year in range(2016, 2018):
        path = "C:\\Users\\jvega\\Documents\\JACCJournalsData\\WebsiteToText\\" + journal + "\\" + journal
        path += str(year)
        print(path)
        files = walk(path)
        for (dirtpath, dirnames, filenames) in files:
            print(filenames)
            for filename in filenames:
                JaccFile = open(path + "\\" + filename, "r", encoding='utf-8')
                fileMetadata = []
                print(path + "\\" + filename)
                for line in JaccFile:
                    for meta in metadataToDownload:
                        if("<meta name=" + meta) in line:
                            print(line)
                            name = ''
                            for j in range(line.index('name=\"') + 6, line.index('content=\"') - 2):
                                name += line[j]
                            print(name)
                            content = ""
                            for k in range(line.index("content=\"") + 9, line.index("/>") - 2):
                                content += line[k]
                            print(content)
                            fileMetadata.append(content)
                a.writerow(fileMetadata)
fp.close()

time.sleep(100)
