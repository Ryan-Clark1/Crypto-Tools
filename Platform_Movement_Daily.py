import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
from colorama import Fore, Back
b = datetime(2021, 6, 23, 17, 1)

i = 0
while i < 1:
    a = datetime.now()
    current_time = a.strftime("%H:%M")
    run_time = b.strftime("%H:%M")
    if current_time == run_time:
        link_ = "https://coinmarketcap.com/rankings/exchanges/"
        html = requests.get(link_).content
        soup = BeautifulSoup(html, 'html.parser')
        extract = soup.find('div', class_='sc-57oli2-0 dEqHl cmc-body-wrapper')
        ex = extract.find('div', class_='tableWrapper___3utdq cmc-table-exchange-rankings-wrapper___1MDxz')
        link_list = []
        for line in ex:
            for element in line:
                for cell in element:
                    if cell.find('img') is None:
                        pass
                    else:
                        link_list.append(cell.find('a').get('href'))
        cset = []
        for link in link_list:
            link_ = "https://coinmarketcap.com" + link
            html = requests.get(link_).content
            soup = BeautifulSoup(html, 'html.parser')
            extract = soup.find('div', class_="tableWrapper___3utdq cmc-table-currencies-markets-wrapper___3D-Cz")
            table = extract.find('table')
            exchange = link[link.index('ges/') + 4:len(link) - 1]
            for line in table:
                for cell in line:
                    placehold = []
                    for element in cell:
                        placehold.append(element.get_text())
                    placehold.append(exchange)
                    date = datetime.today()
                    placehold.append(date)
                    cset.append(placehold)
        headers = cset[0]
        data = cset[1:]
        headers.pop()
        headers.pop()
        headers.append('Exchange')
        headers.append('Date')
        df = pd.DataFrame(data, columns=headers)
        date = datetime.today()
        m = date.month
        d = date.day
        y=date.year
        df.to_excel(r'C:\Users\Ryan\Crypto\R&D\Market\Crypto_Platform_Movement_' + str(d) + "_" + str(m) + "_" +  str(y) + '.xlsx')
        print(Fore.GREEN + Back.LIGHTMAGENTA_EX + "Saved to excel")
        print(Fore.GREEN + "DONE SCANNING")
        time.sleep(86280)
    else:
        time.sleep(random.uniform(50, 60))
        print(Fore.RED + Back.LIGHTCYAN_EX + "Run time not yet met, current time:"+str(current_time)+" Run time set to: "+str(run_time))
        pass

