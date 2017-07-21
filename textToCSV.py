import time
import re #Look up about re to use to find n occurences
from os import listdir
from os import walk
import glob

path = "C:\\Users\\jvega\\Documents\\JACCJournalsData\\WebsiteToText\\JACC1984"

files = walk("C:\\Users\\jvega\\Documents\\JACCJournalsData\\WebsiteToText\\JACC1984")

allTextFilesList = []

metadataToDownload = ['citation_doi', 'citation_volume', 'citation_issue', 'citation_firstpage']

for (dirtpath, dirnames, filenames) in files:
    #JaccFile = filenames
    print(filenames)
    for filename in filenames:
        textFileList = []
        JaccFile = open(path + "\\" + filename, "r")
        for line in JaccFile:
            #if("<meta" in line)
            lineSen = ""
            for i in range(0, len(line)):
                if(i < len(line)):
                    lineSen += line[i]
                else:
                    continue
            print(path + "\\" + filename)
            for meta in metadataToDownload:
                if("<meta" + meta) in lineSen:
                    name = ''
                    for j in range(lineSen.index('name\"') + 6, lineSen.index('content=\"') - 2):
                        name += lineSen[j]
                    print(name)
                    content = ""
                    for k in range(lineSen.index("content=\"") + 9, lineSen.index("/>") - 2):
                        content += lineSen[k]
                    print(content)


time.sleep(100)
