import time
import os
from os import listdir
from os import walk
import csv

metadataToDownload = ['\"citation_doi\"', '\"citation_volume\"', '\"citation_issue\"', '\"citation_firstpage\"']
journals = ['JACC', 'INT', 'IMG', 'BTS', 'EP', 'HF']

#This program should be grouped with the folders that contain the different jacc journals data. It shouldn\'t be in a specific jacc journal folder or a specific year of a jacc journal folder.
print('!!!This program should be grouped with the folders that contain the different jacc journals data. It shouldn\'t be in a specific jacc journal folder or a specific year of a jacc journal folder.!!!')
print('!!!You may need to change the code in this base on what you want to get out of the text files!!!')

print('This program will retrieve the metadata: ')
for title in metadataToDownload:
    print(title)
print('\n')

print('JACC - Journal of American College of Cardiology\nBTS - Basic to Translational Science\nIMG - Cardiovascular Imaging\nINT - Cardiovascular Interventions\nEP - Clinical Electrophysiology\nHF - Heart Failure\n')
journal = ''

while(journal != 'JACC' or journal != 'BTS' or journal != 'IMG' or journal != 'INT' or journal != 'EP' or journal != 'HF'):
    journal = input('Please choose the journal you\'d like to update: ')
    journal = journal.upper()
    if(journal in JACCJournals):
        break
    else:
        print("Invalid Response\n")
        continue


with open((journal + 'JournalData.csv'), 'w', encoding='utf-8', newline='') as fp: #Creates a new csv under the journal name you created
    a = csv.writer(fp, delimiter=',')
    a.writerow(metadataToDownload) # Writes the Titles in the CSV
    for year in range(2016, 2018):
        path = os.getcwd() + '\\' + journal + '\\' + journal #Gets the path of the script then adds the journal folder and then the journal's year folder
        # example: path = "C:\\Users\\jvega\\Documents\\JACCJournalsData\\WebsiteToText\\" + journal + "\\" + journal
        path += str(year)
        print(path)
        files = walk(path)
        # Retrieves all the text files' names in the selected journal and year
        for (dirtpath, dirnames, filenames) in files:
            print(filenames)
            for filename in filenames: # Goes through each text file and gets the metadata based on what you want in 'metadataToDownload'
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

print('Program done!')
time.sleep(100)
