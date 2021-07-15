import pandas as pd
import requests
from bs4 import BeautifulSoup


link_ = "https://coinmarketcap.com/historical/"
html = requests.get(link_).content
soup = BeautifulSoup(html, 'html.parser')
link_list = []
extract1 = soup.find_all('div', class_="wsa6uu-0 jctIId")
for line in extract1:
    link_list.append(line.find('a').get('href'))
cset = []
for link in link_list:
    name = "https://coinmarketcap.com" + link
    html = requests.get(name).content
    soup = BeautifulSoup(html, 'html.parser')
    extract1 = soup.find_all('tr', class_="cmc-table-row")
    for td in extract1:
        placeholder = []
        date = link[12:len(link) - 1]
        placeholder.append(date)
        try:
            for dp in td:
                data = dp.get_text()
                el = dp.get('class')
                el1 = el[len(el)-1]
                category = el1[el1.index('by__')+4:]
                if len(data) == 0:
                    print("data miss")
                    pass
                else:
                    placeholder.append(data)
                    print("data appended")
        except:
            pass
        cset.append(placeholder)
print(cset)
headers = ['date', 'id', 'name', 'symbol', 'market cap', 'price', 'circulating supply', '%1h', '%24h', '%7d', 'rand']
df = pd.DataFrame(cset, columns=headers)
df.to_excel(r'C:\Users\Ryan\Crypto\R&D\Market\Crypto_Price_Historical.xlsx')
print("Saved to excel")
print("DONE SCANNING")
