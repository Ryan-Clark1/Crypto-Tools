import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import unicodedata
import datetime

name = "https://coincodex.com"
link = name
html = requests.get(link).content
soup = BeautifulSoup(html, 'html.parser')
extract1 = soup.find('div', class_='coins-container')
e2 = extract1.find('tbody')
link_list = []
for line in e2:
    suffix = line.find('a').get('href')
    prefix = name
    try:
        link = prefix + suffix + 'historical-data/'
        link_list.append(link)
    except:
        pass

headers = ['date', 'open', 'hi', 'low', 'close', 'volume', 'market cap', 'coin']
xset = []
for link in link_list:
    html = requests.get(link).content
    soup = BeautifulSoup(html, 'html.parser')
    extract1 = soup.find('div', class_='col main-col')
    e2 = extract1.find('table')
    e3 = e2.find_all('td')
    dset = []
    for element in e3:
        data = element.get_text()
        data = unicodedata.normalize('NFKD', data).encode('ascii', 'ignore')
        dset.append(data)
    cset = []
    for obj in dset:
        obj = ''.join(map(chr, obj))
        cset.append(obj)
    i = 0
    n = 0
    bset = []
    while i < len(cset):
        n = 0
        line = []
        while n < 7:
            header = headers[n]
            data = cset[i]
            line.append(data)
            n += 1
            i += 1
        bset.append(line)

    coin = link.find('crypto')
    inter = link[coin:]
    h = inter.find("/")
    start = h + coin + 1
    nb = link[start:]
    end = nb.index("/")
    coin_name = nb[:end]
    for line in bset:
        line.append(coin_name)
        xset.append(line)
    print("Coin: "+ coin_name + " Scanned")
df = pd.DataFrame(xset, columns=headers)
date_start = datetime.date.today() - datetime.timedelta(21)
date_end = datetime.date.today()
df.to_excel(r'C:\Users\Ryan\Crypto\R&D\Market\Crypto_Price_'+ str(date_start) + "_to_"+ str(date_end) +'.xlsx')
print("Saved to excel")
print("DONE SCANNING")






