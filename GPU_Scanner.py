import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
from colorama import Fore, Back

def load_excel(path, file, sheet):
    os.getcwd()
    os.chdir(path)
    file = file
    sheet = sheet
    data = pd.ExcelFile()

set = []
os.getcwd()
os.chdir('C:/Users/Ryan/Crypto/R&D/')
file = 'GPU_Requirements_Coin_Calendar.xls'
sheet = 'link_table'
data = pd.ExcelFile(file)
df = data.parse(sheet)
for row in df.iterrows():
    for char in row:
        set.append(char)
masterset = []
n = 1
z = 0
while n < len(set):
    subset = []
    while z < 6:
        subset.append(set[n][z])
        z += 1
    masterset.append(subset)
    z = 0
    n += 2
i = 0
list_links = []
for cell in masterset:
    if type(cell[3]) == float:
        search_string = str(cell[0])+"+" + str(cell[1])+"+" + str(cell[2])+"+" + str(cell[4])+"gb"
        item = (str(cell[0]) + " " + str(cell[1]) + str(cell[2]) + " " + str(cell[4])
                + "Gb")
        statement = ("Collecting Links for: " + item + " for no more than $" + str(cell[5]))
        name = "https://www.newegg.com/p/pl?d=" + search_string
    else:
        search_string = str(cell[0]) + "+" + str(cell[1]) + "+" + str(cell[2]) + "+" + str(cell[3])+"+" + str(cell[
            4]) + "gb"
        item = (str(cell[0]) + " " + str(cell[1]) + str(cell[2]) + " " + str(
            cell[3]) + " " + str(cell[4]) + "Gb")
        statement = ("Collecting Links for: " + item + " for no more than $" + str(cell[5]))
        name = "https://www.newegg.com/p/pl?d=" + search_string
    print(statement)
    try:
        link = name
        html = requests.get(link).content
        soup = BeautifulSoup(html, 'html.parser')
        extract1 = soup.find('div', class_='list-wrap')
        sift = extract1.findChildren()
        for thing in sift:
            try:
                e1 = thing.find('a', class_="item-title")
                list_links.append(e1.get("href"))
            except:
                pass
    except:
        pass
    list_links = list(dict.fromkeys(list_links))

print("**************************************************************************************Links Collected, Scanning Prices**************************************************************************************")
entries = []
name_list = []
price_list = []
for link in list_links:
    try:
        html = requests.get(link).content
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.find('h1', class_="product-title")
        price = soup.find('ul', class_="price")
        price = price.get_text()
        price = price[1:int(price.find('.')) + 3]
        price = float(price)
        item_name = name.get_text()
        index = item_name.find(' ')
        MANUFACTURER = item_name[:index]
        index = item_name.find('Ge')
        BRAND = item_name[index:index + 7]
        index = item_name.find('TX')
        GPU_TYPE = item_name[index - 1:index + 2]
        index = item_name.find('TX')
        MODEL = item_name[index + 3:index + 7]
        GENERATION = MODEL[0]
        EDITION = MODEL[2:]
        try:
            index = item_name.find('GB')
            MEMORY = item_name[index - 1:index + 2]
        except:
            index = item_name.find(' GB')
            MEMORY = item_name[index - 1:index + 2]
        KEY = str(GPU_TYPE + MODEL + MEMORY[0])
        entry = [item_name, price, GPU_TYPE, MODEL, MEMORY, MANUFACTURER, BRAND, GENERATION, EDITION, link, KEY]
        entries.append(entry)
        print(Fore.CYAN + Back.RESET + "Yum Yum Data for: " + item_name)
    except:
        print(Fore.RED + Back.LIGHTRED_EX + "XxXxX fuck off newegg XxXxX")

td = datetime.date.today()
headers = ['Name', 'Price', 'GPU_TYPE', 'MODEL', 'MEMORY', 'MANUFACTURER', 'BRAND', 'GENERATION', 'EDITION', 'Link', 'Key']
df_write = pd.DataFrame(entries, columns=headers)
file_name = r'C:\Users\Ryan\Crypto\R&D\Hardware\GPU_Scanner_Output_'+ str(td) +'.xlsx'
read_file_name = 'C:\\Users\\Ryan\\Crypto\\R&D\\Hardware\\GPU_Scanner_Output_'+ str(td) +'.xlsx'
df_write.to_excel(file_name)
print(Fore.GREEN + Back.RESET + "Saved to excel")

#sheet = 'Sheet1'
#data1 = pd.ExcelFile(read_file_name, engine='openpyxl')
#df1 = data1.parse(sheet)

#inner_join = pd.merge(df, df1, on='Key', how='inner')
#quick_score = []
#for line in inner_join:
#    p = inner_join['Price']
#    p = pd.to_numeric(p)
#    mp = inner_join['Mining Performance']
#    mp = pd.to_numeric(mp)
#    dec = mp / p
#    calc = dec*1000
#    inner_join['Quick Score'] = calc

#inner_join.to_excel(r'C:\Users\Ryan\Crypto\R&D\Hardware\GPU_Scanner_Output_'+ str(td) +'_fin.xlsx')
os.getcwd()
os.chdir('C:/Users/Ryan/Crypto/R&D/')
file = 'GPU_Requirements_Coin_Calendar.xls'
sheet = 'link_table'
data = pd.ExcelFile(file)
df = data.parse(sheet)
os.getcwd()
os.chdir('C:/Users/Ryan/Crypto/R&D/Hardware')
file = 'GPU_Scanner_Output_'+str(td)+'.xlsx'
sheet = 'Sheet1'
data1 = pd.ExcelFile(file, engine='openpyxl')
df1 = data1.parse(sheet)
inner_join = pd.merge(df, df1, on='Key', how='inner')
quick_score = []
for line in inner_join:
    p = inner_join['Price']
    p = pd.to_numeric(p)
    mp = inner_join['Mining Performance']
    mp = pd.to_numeric(mp)
    dec = mp / p
    calc = dec*1000
    inner_join['Quick Score'] = calc

headers = ['Name', 'Price', 'GPU_TYPE', 'MODEL', 'MEMORY', 'MANUFACTURER', 'BRAND', 'GENERATION', 'EDITION', 'Link']
inner_join.to_excel(r'C:\Users\Ryan\Crypto\R&D\Hardware\GPU_Scanner_Output_'+str(td)+'_fin.xlsx')

print(Fore.GREEN + Back.RESET + "Saved to excel")
print(Fore.YELLOW + "DONE SCANNING")