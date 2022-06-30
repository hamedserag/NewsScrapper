import csv
import re
import pandas as pd
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=360)
from tqdm import tqdm
#███████████████████████████████████████████████████████████████████████████████
def trendingSearches(country,words):
    data = pytrends.trending_searches(pn=country)
    return data[:words]
#███████████████████████████████████████████████████████████████████████████████
def filterDataframe (df):
    return re.sub(r",+",",",(re.sub(r"\d+", ",", str(df)).replace("\n","").replace("  ","")))
#███████████████████████████████████████████████████████████████████████████████
countriesNames = list()
WORDS_PER_COUNTRY = 2
with open ("settingsTS.txt", "r") as myfile:
    data = myfile.read().splitlines()
    WORDS_PER_COUNTRY = int(data[0].split(":")[1])
    del data[0]
    for c in data:
        country = c.split(",")
        if(country[1] == "1"):
            countriesNames.append(country[0])
print(countriesNames)
#███████████████████████████████████████████████████████████████████████████████
trendingList = list()
i=0
for country in tqdm(countriesNames):
    lst = [country,filterDataframe(trendingSearches(country,WORDS_PER_COUNTRY))]
    trendingList.append(lst)
    i+=1
#███████████████████████████████████████████████████████████████████████████████
df = pd.DataFrame(trendingList)
df.to_csv("searchkeywords.csv",mode='a',index=False)