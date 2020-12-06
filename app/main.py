from typing import List

from fastapi import Depends, FastAPI, HTTPException, Path

from bs4 import BeautifulSoup

import datetime
import json
import pandas
import requests
import urllib.request

app = FastAPI()

@app.get("/setmaiinfo")
def main():
    def set_info():
        page = urllib.request.urlopen('https://marketdata.set.or.th/mkt/marketsummary.do?market=SET&language=en&country=US')
        soup = BeautifulSoup(page, 'html.parser')
        table_rows = soup.findAll('div', attrs={'class': 'row info'})
        l = []
        for tr in table_rows:
            td = tr.find_all('div')
            row = [tr.text.replace(" ","").replace("*","").replace("\r","").replace("\n","") for tr in td]
            if len(row) > 0:
                l.append(row)
        df = pandas.DataFrame(l, columns=['name','value'])
        df = df.set_index('name').drop('IndexPerformance')
        return df.to_json().replace("\\","")
    
    def mai_info():
        page = urllib.request.urlopen('https://marketdata.set.or.th/mkt/marketsummary.do?market=mai&language=en&country=US')
        soup = BeautifulSoup(page, 'html.parser')
        table_rows = soup.findAll('div', attrs={'class': 'row info'})
        l = []
        for tr in table_rows:
            td = tr.find_all('div')
            row = [tr.text.replace(" ","").replace("*","").replace("\r","").replace("\n","") for tr in td]
            if len(row) > 0:
                l.append(row)
        df = pandas.DataFrame(l, columns=['name','value'])
        df = df.set_index('name').drop('IndexPerformance')
        return df.to_json().replace("\\","")
    try:
        data = { 'set' : json.loads(set_info())['value'], 'mai' : json.loads(mai_info())['value'] }
        result =  json.dumps(data, indent=4, sort_keys=True)
    except:
        result = {"status":"FAILURE","message":"Can't get data"}
        
    return result