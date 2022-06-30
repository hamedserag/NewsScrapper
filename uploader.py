from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import re
import csv
import pandas as pd
import numpy as np
import urllib.parse
from tqdm import tqdm
import time
df = pd.read_csv('news.csv')
df.columns=["link","header","article","country","keyword"]

df.dropna(subset = ["article"], inplace=True)

data = df.to_numpy()
def getWebpage(link):
    if(len(link) >= 2000):
        print("Uri len is too big : " +str(len(link)))
        print(link)
        return 0
    req = Request(link)
    webpage = urlopen(req).read()
    return webpage
root="http://linkedinn.website/api/post.php/?key="
apikey="lordHSNH2022314HNSHdrol"
lk="&link="
hd="&head="
at="&article="
ct="&country="

artroot="http://linkedinn.website/api/postarticle.php/?id="

articleSize = 1500
for article in tqdm(data):
    link = root+apikey
    if(len(str(article[2])) > 150):
        link+=lk+urllib.parse.quote(str(article[0]))+hd+urllib.parse.quote(str(article[1]))+ct+urllib.parse.quote(str(article[3]))
        web = getWebpage(link)
        postid = str(web).split("'")[1]
        articleURLencoded = str(urllib.parse.quote(str(article[2])))

        iterations = len(articleURLencoded)/articleSize
        lstArt = list()
        artLink = artroot+postid
        #print(len(artLink))
        i=0
        while(i < iterations):
            web = getWebpage(artLink+at+str(articleURLencoded)[(0+(articleSize*i)):(1000+(articleSize*i))])
            i += 1
            #print(web)
            #print(len(articleURLencoded[(0+(1000*i)):(1000+(1000*i))]))
web = getWebpage("http://linkedinn.website/api/cleaner.php")
import os
os.remove('news.csv')
