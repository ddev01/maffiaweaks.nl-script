import requests
from bs4 import BeautifulSoup
import time
import lxml
import re

url_counter = 1
loginurl = 'http://www.maffiaweaks.nl/login'
secure_url = 'http://www.maffiaweaks.nl/'
inbox_url = []
payload = {
    'username': '',
    'password': '',
    'submit': 'Inloggen'
}
foundlist = []
hoeveellinks = int(input('Hoeveel links: ')) + 1
while url_counter < hoeveellinks:
    inbox_url.append('http://www.maffiaweaks.nl/mail/inbox/page/' + str(url_counter))
    url_counter += 1

for x in range(0,4):
    for url in inbox_url:
        with requests.session() as s:
            s.post(loginurl, data=payload)
            r = s.get(url)
            soup = BeautifulSoup(r.content, 'lxml')
            find_table = soup.find_all('table', class_ = 'content_table')
            found_table = find_table[2]
            findcell = found_table.find_all('tr')
            del findcell[0]
            for item in findcell:
                baba = item.find_all('td', class_ = 'tcell')
                if 'gevonden' in baba[1].text:
                    m_username = baba[1].text
                    booboo = item.find_all('a', href=True)
                    mail_link = ''
                    for item in booboo:
                        mail_link = item['href']
                    p = s.get('http://www.maffiaweaks.nl/' + mail_link)
                    soup2 = BeautifulSoup(p.content, 'lxml')
                    m_table = soup2.find_all('table', class_='content_table')
                    m_table_f = m_table[2]
                    m_text = m_table_f.find_all('td', class_='tcell')
                    m_date = m_table_f.find_all('td', class_='tsub')
                    m_message = m_text[0].text
                    listed = m_message.split()
                    message_date = m_date[3].text
                    message_user = listed[2]
                    message_location = listed[5]
                    if tuple([message_user, message_location, message_date]) not in foundlist:
                        foundlist.append(tuple([message_user, message_location, message_date]))

country_sort = lambda country: country[1]
foundlist.sort(key=country_sort)
for item in foundlist:
    print(f'''
    username: {item[0]}
    Locatie: {item[1]}
    Datum: {item[2]} 
    ''')
countriescount = {}
for item in foundlist:
  if item[1] in countriescount:
    countriescount[item[1]] += 1
  else:
    countriescount[item[1]] = 1
sorted_countries = sorted(countriescount.items(), key=lambda x: x[1], reverse=True)

for i in sorted_countries:
	print(i[0], i[1])
