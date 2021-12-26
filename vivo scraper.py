#!/usr/bin/env python
# coding: utf-8

# In[7]:


import requests
import pandas as pd
import time
import numpy as np

def vivino_scraper(page):
    r = requests.get(
      "https://www.vivino.com/api/explore/explore",
      params = {
          #"country_code": "US",
          #"country_codes[]":"pt",
          "currency_code":"EUR",
          #"grape_filter":"varietal",
          "min_rating":"1",
          "order_by":"price",
          "order":"asc",
          "page": page,
          #"price_range_max":"500",
          "price_range_min":"0",
          #"wine_type_ids[]":"1"
      },
      headers= {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
      }
    )
    
    results = []
    for t in r.json()["explore_vintage"]["matches"]:
        try:
            Winery = t["vintage"]["wine"]["winery"]["name"]
        except:
            Winery = np.nan
        try:
            Wine = f'{t["vintage"]["wine"]["name"]}'
        except:
            Wine = np.nan
        try:
            ratings_average = t["vintage"]["statistics"]["ratings_average"]
        except:
            ratings_average = np.nan
        try:
            ratings_count = t["vintage"]["statistics"]["ratings_count"]
        except:
            ratings_count = np.nan
        try:
            status = t["vintage"]["statistics"]["status"]
        except:
            status = np.nan
        try:
            grapes = t["vintage"]["grapes"]
        except:
            grapes = np.nan
        try:
            is_natural = t["vintage"]["wine"]['is_natural']
        except:
            is_natural = np.nan
        try:
            region = t["vintage"]["wine"]['region']['name']
        except:
            region = np.nan
        try:
            country = t["vintage"]["wine"]['region']['country']['native_name']
        except:
            country = np.nan
        try:
            acidity = t['vintage']['wine']['style']['acidity']
        except:
            acidity = np.nan
        try:
            vintage_type = t['vintage']['wine']['vintage_type']
        except:
            vintage_type = np.nan
        try:
            year = t['vintage']['year']
        except:
            year = np.nan
        try:
            volume_ml = t["price"]['bottle_type']['volume_ml']
        except:
            volume_ml = np.nan
        try:
            Price = t["price"]['amount']
        except:
            Price = np.nan
        try:
            currency = t["price"]["currency"]["code"]
        except:
            currency = np.nan
        try:
            type_ = t["price"]["type"]
        except:
            type_ = np.nan

        record = [Winery, Wine, ratings_average, ratings_count, status, grapes, is_natural, region, country, acidity, vintage_type, year, volume_ml, Price, currency, type_]
        results.append(record)
        dataframe = pd.DataFrame(results,columns=['Winery','Wine','Rating','num_review', 'status', 'grapes', 'is_natural', 'region', 'country', 'acidity', 'vintage_type', 'year', 'volume_ml', 'Price', 'currency', 'type'])
        
    return dataframe


# In[ ]:


page = 1
while True:
    wine_df = vivino_scraper(page)
    if page % 10 == 0:
        print(f"page {page}")
    wine_df.to_csv(f"vivo/page_{page}.csv", index=False)
    page += 1
    time.sleep(2)

    if len(wine_df) == 0:
        break

