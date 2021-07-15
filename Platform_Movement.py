import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
cookbook = []
link_ = "https://coinmarketcap.com/rankings/exchanges/"
html = requests.get(link_).content
soup = BeautifulSoup(html, 'html.parser')
cookbook.append(soup.prettify())
extract = soup.find('div', class_='sc-57oli2-0 dEqHl cmc-body-wrapper')
ex = extract.find('div', class_='h7vnx2-1 bFzXgL')
link_list = []
for line in ex:
    for element in line:
        for cell in element:
            if cell.find('img') is None:
                pass
            else:
                link_list.append(cell.find('a').get('href'))
cset = []

link__ = "https://coinmarketcap.com/exchanges/binance/"
html = requests.get(link_).content
soup__ = BeautifulSoup(html, 'html.parser')
cookbook.append(soup__.prettify())
for link in link_list:
    link_ = "https://coinmarketcap.com" + link
    html = requests.get(link_).content
    soup = BeautifulSoup(html, 'html.parser')
    extract = soup.find('div', class_="sc-16r8icm-0 sc-1xafy60-0 eJJswN")  #This will need to be updated weekly
    table = extract.find('table')
    exchange = link[link.index('ges/')+4:len(link)-1]
    for line in table:
        for cell in line:
            placehold = []
            for element in cell:
                placehold.append(element.get_text())
            placehold.append(exchange)
            date = datetime.date.today()
            placehold.append(date)
            cset.append(placehold)
headers = cset[0]
data = cset[1:]
headers.pop()
headers.pop()
headers.append('Exchange')
headers.append('Date')
df = pd.DataFrame(data, columns=headers)
date = datetime.date.today()
df.to_excel(r'C:\Users\Ryan\Crypto\R&D\Market\Crypto_Platform_Movement_'+str(date)+'.xlsx')
cdf = pd.DataFrame(cookbook)
cdf.to_excel(r'C:\Users\Ryan\Crypto\R&D\Market\Crypto_Platform_Movement_'+ str(date)+'_HTML.xlsx')
print("Saved to excel")
print("DONE SCANNING")