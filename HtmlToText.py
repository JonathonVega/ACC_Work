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
    if "content/68" in article:
        return True
    else:
        return False

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

#allMeta = []
for key in JACCJournal:
    soup = getArchive(JACCJournals[key])
    years = ["2016"]
    for year in years: #soup.find_all("li", {"class": ["year active even", "year active odd"]}): #soup.find_all("li", {"class": ["year even", "year odd", "year active even", "year active odd", "year last even", "year first odd" ]}):
        #print(year.string)
        issues = getIssues(year, JACCJournals[key])
        for issue in issues:
            articles = getArticles(issue, JACCJournals[key])
            for article in articles:
                if skipArticle(article):
                    print(article)
                    #time.sleep(2)
                    continue
                elif (year == "2016" or year == "2017") and (key == "JACC" or key == "IMG" or key == "INT" or key == "EP" or key == "HF"):
                    restrictedArticleSourceToTxt(article, JACCJournals[key])
                else:
                    openArticleSourceToTxt(article, JACCJournals[key])



#createCSV(allMeta)
