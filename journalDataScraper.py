from bs4 import BeautifulSoup
import requests
import csv

# This program is meant to scrape the jacc journal sites without downloading the html source pages, and then inserting the metadata into a CSV.
# This is a longer process when getting the metadata of the articles and I would probably recommend using the script to download the source pages instead.


JACCJournals = {"JACC": "http://www.onlinejacc.org",
"BTS": "http://www.basictranslational.onlinejacc.org",
"IMG": "http://www.imaging.onlinejacc.org",
"INT": "http://www.interventions.onlinejacc.org",
"EP": "http://www.electrophysiology.onlinejacc.org",
"HF": "http://www.heartfailure.onlinejacc.org"}

# This block will get the BeautifulSoup of the journal's archive
def getArchive(journalLink):
    r = requests.get(journalLink + "/content/by/year")
    archiveSoup = BeautifulSoup(r.text, 'lxml')
    return archiveSoup

# This block will return a list of all the links to the issues of a chosen year
def getIssuesList(year, JLink):
        issuesList = []
        site = JLink + "/content/by/year/" + year
        print(site)
        archiveYearSoup = BeautifulSoup((requests.get(site)).text, "lxml")
        for issue in archiveYearSoup.find_all("a", {"class": "hw-issue-meta-data"}):
            issuesList.append(issue.get("href"))
        return issuesList

# There are some Articles in an issue's page that isn't from that certain issue such as the 'Journal Impact' section
# This block will keep these unwanted articles from being downloaded
def isArticleRelatedToIssue(issueLink, href):
    if issueLink in href:
        return True
    else:
        return False

# Returns a list of articles from the selected issue from the chosen Journal
def getArticlesList(issueLink, JLink):
    issueSoup = BeautifulSoup((requests.get(JLink + issueLink)).text, 'lxml')
    articlesList = []
    for article in issueSoup.find_all("a", {"class": "highwire-cite-linked-title"}):
        if isArticleRelatedToIssue(issueLink, article.get("href")):
            articlesList.append(article.get("href"))
            print(article.get("href"))
    return articlesList

# Returns a dictionary of all the metadatas' name and their corresponding content
def getMetaData(articleLink, JLink):
    articleSoup = BeautifulSoup((requests.get(JLink + articleLink)).text, 'lxml')
    metaData = {}
    for meta in articleSoup.find_all("meta"):
        if meta.get("name") is None:
            continue
        elif meta.get("name") == "citation_author":
            break
        if meta.get("name") in metaData:
            metaData[meta.get("name")] = metaData[meta.get("name")] + "|" + meta.get("content")

        else:
            metaData[meta.get("name")] = meta.get("content")
    return metaData

# Retunr a list of all the metadatas to put into the CSV
def getDataTitlesList(metaData):
    dataTitles = []
    for k in metaData[0]:
        dataTitles.append(k)
    return dataTitles #Returns a list

# This block will create a CSV of the certain year of the journals
def createCSV(year, metaDataListOfDictionaries):
    with open(('JACCJournals' + year + '.csv'), 'w', encoding = "utf-8", newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        dataTitles = getDataTitlesList(metaDataListOfDictionaries) #Returns list of all the Titles/Labels
        data=[]
        data.append(dataTitles)
        for articleMeta in metaDataListOfDictionaries:
            articleMetaList = []
            for k in dataTitles:
                if k == "citation_abstract" and k in articleMeta:
                    articleMeta[k].replace("<p>", "")
                    articleMeta[k].replace("</p>", "")
                    articleMeta[k].replace("<h3>", "")
                    articleMeta[k].replace("</h3>", "")
                    articleMetaList.append(articleMeta[k])
                elif k in articleMeta:
                    articleMetaList.append(articleMeta[k])
                else:
                    articleMetaList.append("")
            data.append(articleMetaList)
        a.writerows(data)
    fp.close()

allMeta = [] # This is where a very long list of all the articles' metadatas will be
print('!!!This Journal will retrieve all metadata from all journals of a chosen year, and then place them into a CSV!!!')
print('!!!I would recommend using the script to download all the source pages of the articles!!!')
print('JACC - Journal of American College of Cardiology\nBTS - Basic to Translational Science\nIMG - Cardiovascular Imaging\nINT - Cardiovascular Interventions\nEP - Clinical Electrophysiology\nHF - Heart Failure')
journal = ''

# This block was made to make sure a valid journal is chosen by the user
while(journal != 'JACC' or journal != 'BTS' or journal != 'IMG' or journal != 'INT' or journal != 'EP' or journal != 'HF'):
    journal = input('Please choose the journal you\'d like to update: ')
    journal = journal.upper()
    if(journal in JACCJournals):
        break
    else:
        print("Invalid Response\n")
        continue

# This block will begin retrieving the metadata from the jacc journals' articles
year = ''
for key in JACCJournals:
    soup = getArchive(JACCJournals[key])
    year = input('What year you would like to update\nExample:\"2017\"\nChoose your Year: ')
    issues = getIssuesList(year, JACCJournals[key])
    for issue in issues:
        articles = getArticlesList(issue, JACCJournals[key])
        for article in articles:
            metaDataPassing = []
            allMeta.append(getMetaData(article, JACCJournals[key])) # Returns a dictionary
            print(getMetaData(article, JACCJournals[key]))
        print(allMeta)


createCSV(year, allMeta)
