from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import re
import csv
import pandas as pd
import numpy as np
import urllib.parse
from tqdm import tqdm
#███████████████████████████████████████████████████████████████████████████████la 
root = 'https://news.google.com/search?q='
articleRelDir = "./articles/"
articleAbsDir = "https://news.google.com/articles/"
#███████████████████████████████████████████████████████████████████████████████
def filterAnchorTag(tag):
    return str(tag).split("href=")[1].split('\"')[1]
#███████████████████████████████████████████████████████████████████████████████
def getWebpage(link):
    req = Request(link)
    webpage = urlopen(req).read()
    with requests.Session() as c:
        soup = BeautifulSoup(webpage, 'html5lib')
        return soup
#███████████████████████████████████████████████████████████████████████████████
def getRedirectionPage(link):
    soup = getWebpage(link)
    tag = soup.find('a', attrs={"rel":"nofollow"})
    soup = getWebpage(filterAnchorTag(tag))
    return soup
#███████████████████████████████████████████████████████████████████████████████
def getArticlefromSoup(soup):
    article = ""
    for tag in soup.find_all('p'):
        article += tag.text
    return article
#███████████████████████████████████████████████████████████████████████████████
def fetchLinks(link):
    soup = getWebpage(link)
    articlesLst = list()
    for item in soup.find_all('a', attrs={'class': 'DY5T1d'}):
        filteredLink = filterAnchorTag(item).replace(articleRelDir,articleAbsDir)
        lst = [filteredLink, item.text]
        articlesLst.append(lst)
    return articlesLst
#███████████████████████████████████████████████████████████████████████████████
def fetchArticles(articlesLst,country,keyword,maxArticles):
    i=1
    failedLinks = list()
    length = len(articlesLst)
    for item in tqdm(articlesLst,desc="Articles"):
        try:
            soup = getRedirectionPage(item[0])
            article = getArticlefromSoup(soup)
            item.append(article)
            item.append(country)
            item.append(keyword)
            i+=1
            if(i == maxArticles):
                break
        except:
            articlesLst.remove(item)
            item.append(country)
            item.append(keyword)
            failedLinks.append(item)
    return failedLinks
#███████████████████████████████████████████████████████████████████████████████
def saveArticles(articlesLst):
    df = pd.DataFrame(articlesLst)
    df.to_csv("news.csv",mode='a',header=True,index=False)
def saveFailedLinks(failedLinks):
    df = pd.DataFrame(failedLinks)
    df.to_csv("failednewslinks.csv",mode='a',header=True,index=False)
#███████████████████████████████████████████████████████████████████████████████
ARTICLES_PER_WORD = 2
with open ("settingsWS.txt", "r") as myfile:
    data = myfile.read().splitlines()
    ARTICLES_PER_WORD = int(data[0].split(":")[1])
#███████████████████████████████████████████████████████████████████████████████
def ArticleFetcher():
    df = pd.read_csv("searchkeywords.csv")
    dataList = df.to_numpy()
    for countryData in dataList:
        print(str(countryData[0]))
        keywords = str(countryData[1]).split(",")
        
        df=df.drop([0])
        df.to_csv("searchkeywords.csv",mode='w',header=True,index=False)
        
        for keyword in keywords:
            if(keyword == " " or keyword == ""):
                continue
            print("searching for :" + str(keyword))
            language = "&gl="+countryData[0]+"&ceid="+countryData[0]
            link = root+urllib.parse.quote(keyword)+language

            articlesLst = fetchLinks(link)
            failedLinks = fetchArticles(articlesLst,str(countryData[1]),str(keyword),ARTICLES_PER_WORD)
            saveArticles(articlesLst)
            saveFailedLinks(failedLinks)
#███████████████████████████████████████████████████████████████████████████████
ArticleFetcher()