import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import joblib

COLUMNS = ['floor', 'total_floor_num', 'room_num', 'area', 'year',
       'year_renovation', 'top_floor', 'oldtown', '0', 'antakalnyje',
       'aukstuosiuose-paneriuose', 'avizieniuose', 'bajoruose', 'balsiuose',
       'baltupiuose', 'burbiskes', 'fabijoniskese', 'filaretuose',
       'grigiskese', 'jeruzaleje', 'justiniskese', 'kalnenuose',
       'karoliniskese', 'lazdyneliuose', 'lazdynuose', 'markuciuose',
       'naujamiestyje', 'naujininkuose', 'naujojoje-vilnioje', 'pasilaiciuose',
       'pavilnyje', 'pilaiteje', 'santariskese', 'sauletekyje', 'senamiestyje',
       'seskineje', 'siaures-miestelyje', 'snipiskese', 'tarandeje', 'traku',
       'uzupyje', 'valakampiuose', 'verkiuose', 'vilkpedeje', 'virsuliskese',
       'visoriuose', 'zemuosiuose-paneriuose', 'zirmunuose', 'zveryne']

# PAGE = "https://www.aruodas.lt/butu-nuoma-vilniuje-fabijoniskese-salomejos-neries-g-isnuomojamas-dveju-kambariu-butas-esantis-4-955971/"

DICT_FOR_DF_RENAME = {"Aukštas:": "floor", "Aukštų sk.:": "total_floor_num",
                   "Kambarių sk.:":"room_num", "Metai:":"year_full",
                   "Plotas:":"area","Pastato tipas:":"house_type", 
                  "Šildymas:":"heating", "Apsauga:": "security",
                   "Ypatybės:":"general"
                  }

DISTRICTS = ["pasilaiciuose", "zveryne", "pilaiteje", "senamiestyje", 
             "naujamiestyje", "uzupyje", "snipiskese", "antakalnyje",
            "zirmunuose","lazdyneliuose", "karoliniskese", "naujojoje-vilnioje", "tarandeje","seskineje",
             "grigiskese", "santariskese", "balsiuose", "siaures-miestelyje",
             "markuciuose", "virsuliskese","fabijoniskese", "valakampiuose",
             "baltupiuose","justiniskese","visoriuose","lazdynuose","jeruzaleje"
             ,"avizieniuose","filaretuose","kalnenuose",
             "pavilnyje","bajoruose", "burbiskes","naujininkuose","vilkpedeje",
             "zemuosiuose-paneriuose","aukstuosiuose-paneriuose","jeruzaleje","sauletekyje","traku","verkiuose"
            ]


def ScrapeFlat(page):
    d = {}
    d["Adresas"] = page
    html_file = requests.get(page)
    soup = BeautifulSoup(html_file.text, "html.parser")
    dd = soup.select("dd")
    dt = soup.select("dt")
    for i in range(20):
        try:
            tmp_val = str(dd[i].getText()).strip()
            tmp_name = str(dt[i].getText()).strip()
            d[tmp_name] = tmp_val
        except:
            return d
    return d

def CreateDataFrameHeader(COLUMNS):    
    return pd.DataFrame(columns=COLUMNS)



def FromDictToDF(d):
    dfFlat = pd.DataFrame()
    dfFlat = dfFlat.append(d, ignore_index=True)
    return dfFlat

def CleanDF(dfFlat):    
    dfFlat = dfFlat.rename(columns={"Aukštas:": "floor", "Aukštų sk.:": "total_floor_num",
                   "Kambarių sk.:":"room_num", "Metai:":"year_full",
                   "Plotas:":"area","Pastato tipas:":"house_type", 
                  "Šildymas:":"heating", "Apsauga:": "security",
                   "Ypatybės:":"general"})    
    try:
        dfFlat[['year','year_renovation']] = dfFlat['year_full'].str.split(',',expand=True)
        dfFlat['year'] = dfFlat['year_full'].str[:4]
        dfFlat['year'].fillna(dfFlat["year_full"],inplace = True)
        dfFlat["year"] = pd.to_numeric(dfFlat["year"],downcast='integer')
        dfFlat['year_renovation'] = dfFlat['year_renovation'].str[:5]
        dfFlat["year_renovation"] = pd.to_numeric(dfFlat["year_renovation"],downcast='integer')
    except:
        dfFlat['year'] = dfFlat['year_full'].str[:4]
        dfFlat['year_renovation'] = 0
        
    dfFlat['area'] = dfFlat['area'].str.replace(' m²','')
    dfFlat['area'] = dfFlat['area'].str.replace(',','.')
    return dfFlat

def predictPrice(PAGE):
    d = ScrapeFlat(PAGE)
    dfFlat = FromDictToDF(d)

    dfFlat = CleanDF(dfFlat)
    df = CreateDataFrameHeader(COLUMNS)

    dfFlat = df.append(dfFlat, ignore_index=True)
    
    for district in DISTRICTS:
        dfFlat.loc[dfFlat[dfFlat['Adresas'].str.contains(district).values].index, district] = 1
        dfFlat[district].fillna(value = 0, inplace = True)
 
    dfFlat = dfFlat[COLUMNS]
    dfFlat.fillna(value = 0, inplace = True)
    model = joblib.load('model.pkl')
    return [model.predict(dfFlat)[0], d["Kaina mėn.:"]]
