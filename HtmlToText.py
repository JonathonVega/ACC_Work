from bs4 import BeautifulSoup
import urllib.request
import requests
import csv
from requests.auth import HTTPBasicAuth
import time

JACCJournal = {"JACC": "http://www.onlinejacc.org"}
INTJournal = {"INT":"http://www.interventions.onlinejacc.org"}
BTSJournal = {"BTS": "http://www.basictranslational.onlinejacc.org"}
IMGJournal = {"IMG": "http://www.imaging.onlinejacc.org"}
EPJournal = {"EP": "http://www.electrophysiology.onlinejacc.org"}
HFJournal = {"HF": "http://www.heartfailure.onlinejacc.org"}

otherJournals = {"BTS": "http://www.basictranslational.onlinejacc.org",
"IMG": "http://www.imaging.onlinejacc.org",
"EP": "http://www.electrophysiology.onlinejacc.org",
"HF": "http://www.heartfailure.onlinejacc.org"}

JACCJournals = {"JACC": "http://www.onlinejacc.org",
"BTS": "http://www.basictranslational.onlinejacc.org",
"IMG": "http://www.imaging.onlinejacc.org",
"INT": "http://www.interventions.onlinejacc.org",
"EP": "http://www.electrophysiology.onlinejacc.org",
"HF": "http://www.heartfailure.onlinejacc.org"}

skipArticlesList = ['/content/48/5/e247', '/content/50/7/e1', '/content/52/13/e1', '/content/48/4/e149', '/content/48/3/e1','/content/50/17/e159', '/content/61/23/e179', '/content/60/24/e44', '/content/58/24/e123'] #The links to these pages don't work

def getArchive(journalLink):
    r = requests.get(journalLink + "/content/by/year")
    archiveSoup = BeautifulSoup(r.text, 'lxml')
    return archiveSoup

def getIssues(year, JLink):
        issues = []
        site = JLink + "/content/by/year/" + year
        print(site)
        archiveYearSoup = BeautifulSoup((requests.get(site)).text, "lxml")
        for issue in archiveYearSoup.find_all("a", {"class": "hw-issue-meta-data"}):
            issues.append(issue.get("href"))
        return issues

def isArticleRelatedToIssue(issueLink, href):
    if issueLink in href:
        return True
    else:
        return False

def getArticles(issueLink, JLink):
    issueSoup = BeautifulSoup((requests.get(JLink + issueLink)).text, 'lxml')
    articles = []
    for article in issueSoup.find_all("a", {"class": "highwire-cite-linked-title"}):
        if isArticleRelatedToIssue(issueLink, article.get("href")):
            articles.append(article.get("href"))
            print(article.get("href"))
    return articles

def getDataTitlesList(metaData):
    dataTitles = []
    for k in metaData[0]:
        dataTitles.append(k)
    return dataTitles

def skipArticle(article): # Should only be used when you want to skip to an issue
    if "content/4/2/" in article or "content/4/1/" in article:
        return False
    else:
        return True

def restrictedArticleSourceToTxt(articleLink, JLink):
    with requests.Session() as c:
        USERNAME = 'XXX'
        PASSWORD = 'XXX'
        url = 'http://auth.acc.org/ACCFederatedLogin/Login?SP=HW&src=HW&target=http%3A%2F%2Fwww.onlinejacc.org%2Fcontent%2Fby%2Fyear%3Fsso%3D1%26sso_redirect_count%3D1&destination=/content/by/year&_ga=2.92849885.190577121.1499866663-938354422.1499434034'
        c.get(url)
        login_data = dict(UserName=USERNAME, Password=PASSWORD, next='/')
        c.post(url, data=login_data, headers={'Referer': 'http://www.onlinejacc.org'})
        page = c.get(JLink + articleLink)
        fileName = articleLink + ".txt"
        webLink = JLink + articleLink
        print(fileName)
        fileName = fileName.replace("/content", "content")
        fileName = fileName.replace("/","_")
        with open(fileName,"w", encoding='utf-8', newline='') as tf:
            tf.write((page.content).decode('utf-8'))
            tf.close()

def openArticleSourceToTxt(articleLink, JLink):
    fileName = articleLink + ".txt"
    webLink = JLink + articleLink
    print(fileName)
    fileName = fileName.replace("/content", "content")
    fileName = fileName.replace("/","_")
    print(webLink)
    urllib.request.urlretrieve(webLink, fileName)

def stoppedRunning(articleLink):
    stoppedRunning = False
    for i in skipArticlesList:
        if i == articleLink:
            stoppedRunning = True
    return stoppedRunning


# Instructions for the user
print('!!!Make sure this script is inside the folder that you want all the article\'s source code in. Otherwise you\'ll have hundreds of files somewhere that you don\'t want them in. I\'d recommend copying and pasting this program into the folder you want the article\'s source pages in.!!!\n')
print('JACC - Journal of American College of Cardiology\nBTS - Basic to Translational Science\nIMG - Cardiovascular Imaging\nINT - Cardiovascular Interventions\nEP - Clinical Electrophysiology\nHF - Heart Failure')
journal = input('Please choose the journal you\'d like to update: ')
journal = journal.upper()

# This block was made to make sure the right journal is chosen
while(journal != 'JACC' or journal != 'BTS' or journal != 'IMG' or journal != 'INT' or journal != 'EP' or journal != 'HF'):
    journal = input('Please choose a valid journal: ')
    journal = journal.upper()
    if(journal in JACCJournals):
        break
    else:
        continue

print(journal)
soup = getArchive(JACCJournals[journal])
year = input('What year you would like to update\nExample:\"2017\"\nChoose your Year: ')
issues = getIssues(year, JACCJournals[key])
for issue in issues:
    articles = getArticles(issue, JACCJournals[key])
    for article in articles:
        if skipArticle(article):
            continue
        if stoppedRunning(article):
            continue
        elif (year == "2016" or year == "2017") and (key == "JACC" or key == "IMG" or key == "INT" or key == "EP" or key == "HF"):
            restrictedArticleSourceToTxt(article, JACCJournals[key])
        else:
            openArticleSourceToTxt(article, JACCJournals[key])



#createCSV(allMeta)
