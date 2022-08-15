import requests
from bs4 import BeautifulSoup
import time
import lxml
import re
from dhooks import Webhook

hook = Webhook('')
loginurl = 'http://www.maffiaweaks.nl/login'
secure_url = 'http://www.maffiaweaks.nl/'
payload = {
    'username': '',
    'password': '',
    'submit': 'Inloggen'
}
attempts = 0
members_list = ['']
blacklist = ['']
member_links =[]
scraped_members = []
for member in members_list:
    member_links.append('http://www.maffiaweaks.nl/member/' + member)
STOPSTART = 0

notifcounter = 0
gotcha = []

while STOPSTART == 0:
    with requests.session() as s:
        s.post(loginurl, data=payload)
        for link in member_links:
            r = s.get(link)
            soup = BeautifulSoup(r.content, 'lxml')
            find_table = soup.find_all('table', class_ = 'content_table')
            found_table = find_table[2]
            find_td = found_table.find_all('td', class_ = 'tcell')
            m_bescherming = find_td[54].text
            m_username = find_td[2].text
            if m_username not in blacklist:
                if m_bescherming == 'Nee' and find_td[6].find('span', 'rankbar_text').text != ' 0%':
                    m_health = find_td[6].find('span', 'rankbar_text').text
                    m_power = find_td[9].text
                    m_cash = find_td[18].text.replace(' ', '').replace('€', '').replace('.','')
                    m_bank = find_td[24].text.replace(' ', '').replace('€', '').replace('.','')
                    m_total = int(m_cash) + int(m_bank)
                    m_lastseen = find_td[33].text
                    print(f'''
                    Gebruikersnaam: {m_username}
                    Gezondheid: {m_health}
                    Power: {m_power}
                    Cash: {m_cash}
                    Bank: {m_bank}
                    Totaal: {m_total}
                    Bescherming: {m_bescherming}
                    Laatst online: {m_lastseen}
                    ''')
                    if m_username not in gotcha:
                        hook.send(f'''
                        Gebruikersnaam: {m_username}
                        Gezondheid: {m_health}
                        Power: {m_power}
                        Cash: {m_cash}
                        Bank: {m_bank}
                        Totaal: {m_total}
                        Bescherming: {m_bescherming}
                        Laatst online: {m_lastseen}
                        ''')
                        gotcha.append(m_username)

        print('[',attempts,'] Sleeping for 3 seconds...')
        time.sleep(3)
        attempts = attempts + 1
