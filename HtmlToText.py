from bs4 import BeautifulSoup
import urllib.request
import requests
import csv
from requests.auth import HTTPBasicAuth
import time
import datetime

# All the web links to the JACC Journals
JACCJournals = {"JACC": "http://www.onlinejacc.org",
"BTS": "http://www.basictranslational.onlinejacc.org",
"IMG": "http://www.imaging.onlinejacc.org",
"INT": "http://www.interventions.onlinejacc.org",
"EP": "http://www.electrophysiology.onlinejacc.org",
"HF": "http://www.heartfailure.onlinejacc.org"}

skipArticlesList = ['/content/48/5/e247', '/content/50/7/e1', '/content/52/13/e1', '/content/48/4/e149', '/content/48/3/e1','/content/50/17/e159', '/content/61/23/e179', '/content/60/24/e44', '/content/58/24/e123'] #The links to these pages don't work

# Uses Beautiful Soup to retrieve the archive source page from the journal's link
def getArchive(journalLink):
    r = requests.get(journalLink + "/content/by/year")
    archiveSoup = BeautifulSoup(r.text, 'lxml')
    return archiveSoup

# Returns all the issues of the selected year from the chosen Journal in a list
# Example: /content/70/7
def getIssues(year, JLink):
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
def getArticles(issueLink, JLink):
    issueSoup = BeautifulSoup((requests.get(JLink + issueLink)).text, 'lxml')
    articlesList = []
    for article in issueSoup.find_all("a", {"class": "highwire-cite-linked-title"}):
        if isArticleRelatedToIssue(issueLink, article.get("href")):
            articlesList.append(article.get("href"))
            print(article.get("href"))
    return articlesList

# This block should only be used when you don't want the script to download certain articles in issues
# Shouldn't be used at all unless you need to skip or get certain articles without having the script to read the all the issues in that year
def skipArticle(article):
    if "content/4/2/" in article or "content/4/1/" in article:
        return True
    else:
        return False

# This block is meant to get the source pages from articles that are restricted
# Will need to input your JACC USERNAME and PASSWORD to access them
def restrictedArticleSourceToTxt(articleLink, JLink):
    with requests.Session() as c:
        USERNAME = 'XXX'
        PASSWORD = 'XXX'
        url = 'http://auth.acc.org/ACCFederatedLogin/Login?SP=HW&src=HW&target=http%3A%2F%2Fwww.onlinejacc.org%2Fcontent%2Fby%2Fyear%3Fsso%3D1%26sso_redirect_count%3D1&destination=/content/by/year&_ga=2.92849885.190577121.1499866663-938354422.1499434034' # This is the link to the sign-in page
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

# This block is meant to get the source pages from articles that are open-access
def openArticleSourceToTxt(articleLink, JLink):
    fileName = articleLink + ".txt"
    webLink = JLink + articleLink
    print(fileName)
    fileName = fileName.replace("/content", "content")
    fileName = fileName.replace("/","_")
    print(webLink)
    urllib.request.urlretrieve(webLink, fileName)

# This block will ignore the article links inside 'skipArticlesList' since those articles don't work
# Should not be used at all unless you come across recent articles that don't load when clicked, therefore you should include them in 'skipArticlesList' so the program can run for the rest
def stoppedRunning(articleLink):
    stoppedRunning = False
    for i in skipArticlesList:
        if i == articleLink:
            stoppedRunning = True
    return stoppedRunning


# Instructions for the user
print('!!!Make sure this script is inside the folder that you want all the article\'s source code in. Otherwise you\'ll have hundreds of files somewhere that you don\'t want them in. I\'d recommend copying and pasting this program into the folder you want the article\'s source pages in.!!!\n!!!Also make sure that your JACC username and JACC password are in this script in the method \'restrictedArticleSourceToTxt\' so that the program is able to access the restricted content.!!!\n')
print('JACC - Journal of American College of Cardiology\nBTS - Basic to Translational Science\nIMG - Cardiovascular Imaging\nINT - Cardiovascular Interventions\nEP - Clinical Electrophysiology\nHF - Heart Failure')
journal = input('Please choose the journal you\'d like to update: ')
journal = journal.upper()

# This block was made to make sure a valid journal is chosen by the user
while(journal != 'JACC' or journal != 'BTS' or journal != 'IMG' or journal != 'INT' or journal != 'EP' or journal != 'HF'):
    journal = input('Please choose a valid journal: ')
    journal = journal.upper()
    if(journal in JACCJournals):
        break
    else:
        continue

print(journal)
archiveSoup = getArchive(JACCJournals[journal]) #Reads the journal's archive source page
year = input('What year you would like to update\nExample:\"2017\"\nChoose your Year: ')
issuesList = getIssues(year, JACCJournals[journal])
for issue in issuesList:
    articlesList = getArticles(issue, JACCJournals[journal])
    for article in articlesList:
        now = datetime.datetime.now()
        print(now.year)
        print(int(now.year))
        if skipArticle(article):
            continue
        if stoppedRunning(article):
            continue
        elif (year == str((int(now.year) - 1)) or year == str(now.year)) and (journal == "JACC" or journal == "IMG" or journal == "INT" or journal == "EP" or journal == "HF"):
            restrictedArticleSourceToTxt(article, JACCJournals[journal])
        else:
            openArticleSourceToTxt(article, JACCJournals[journal])
