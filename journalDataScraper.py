from bs4 import BeautifulSoup
import requests
import csv

JACCJournal = {"JACC": "http://www.onlinejacc.org"}

INTJournal = {"INT":"http://www.interventions.onlinejacc.org"}

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

def getDataTitlesList(metaData):
    dataTitles = []
    for k in metaData[0]:
        dataTitles.append(k)
    return dataTitles

def createCSV(metaDataListOfDictionaries):
    with open('JACC2007.csv', 'w', encoding = "utf-8", newline='') as fp:
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

allMeta = []
for key in JACCJournal:
    soup = getArchive(JACCJournals[key])
    years = ["2007"]
    for year in years: #soup.find_all("li", {"class": ["year active even", "year active odd"]}): #soup.find_all("li", {"class": ["year even", "year odd", "year active even", "year active odd", "year last even", "year first odd" ]}):
        #print(year.string)
        issues = getIssues(year, JACCJournals[key])
        for issue in issues:
            articles = getArticles(issue, JACCJournals[key])
            for article in articles:
                metaDataPassing = []
                allMeta.append(getMetaData(article, JACCJournals[key])) # Returns a dictionary
                print(getMetaData(article, JACCJournals[key]))
            print(allMeta)


createCSV(allMeta)
