import time
from selenium import webdriver
from selenium.webdriver.common import keys
from pyautogui import *
import pyautogui
import time
import keyboard
import random
from bs4 import BeautifulSoup
import requests
import lxml

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")

url_counter = 3
loginurl = 'http://www.maffiaweaks.nl/login'
secure_url = 'http://www.maffiaweaks.nl/'
list1_url = []
while url_counter < 88:
    list1_url.append('http://www.maffiaweaks.nl/members/page/' + str(url_counter))
    url_counter = url_counter + 1
payload = {
    'username': '',
    'password': '',
    'submit': 'Inloggen'
}

members_list = []

with requests.session() as s:
    s.post(loginurl, data=payload)
    for urls in list1_url:
        r = s.get(urls)
        soup = BeautifulSoup(r.content, 'lxml')
        find_tables = soup.find_all('table', class_ = 'content_table')
        found_table = find_tables[3]
        find_rows = found_table.find_all('tr')
        del find_rows[0] #deletes format table row
        #hier moet de for loop beginnen.
        counter = 0
        for row in find_rows:
            if counter % 5 == 0:
                counter = counter + 1
                deep = row.find_all('td', class_ = 'tcell')
                username = deep[2].text.replace(' ', '').replace('€', '').replace('.','')
                cash_geld = int(deep[15].text.replace(' ', '').replace('€', '').replace('.',''))
                bank_geld = int(deep[17].text.replace(' ', '').replace('€', '').replace('.',''))
                if tuple([username, cash_geld, bank_geld, cash_geld + bank_geld]) not in members_list:
                    members_list.append(tuple([username, cash_geld, bank_geld, cash_geld + bank_geld]))
            else:
                counter = counter + 1
cash_sort = lambda member: member[1]
bank_sort = lambda member: member[2]
total_sort = lambda member: member[3]
members_list.sort(key=total_sort, reverse=True)
for pepepep in members_list:
    print('Username: ',pepepep[0])
    print('Cash geld: ', pepepep[1])
    print('Bank geld: ', pepepep[2])
    print('Totaal: ', pepepep[3])
    print('----------')
login_n = ''
login_p = ''
aantal = int(input('Hoeveel detectives huren?'))
browser = webdriver.Chrome(chrome_options=options)
browser.get('http://www.maffiaweaks.nl/login')
loginbalk = browser.find_elements_by_xpath('//*[@type="text"]')
loginbalk[1].click()
pyautogui.write(login_n, interval=0.05)
loginpass = browser.find_elements_by_xpath('//*[@type="password"]')
loginpass[1].click()
pyautogui.write(login_p, interval=0.05)
pyautogui.press('enter')
time.sleep(3)
for tiem in members_list[:aantal]:
    tiemcounter = 0
    browser.get('http://www.maffiaweaks.nl/detective')
    clickbalk = browser.find_elements_by_xpath('//*[@class="select"]')
    clickbalk[0].click()
    pyautogui.write(tiem[0], interval=0.05)
    pyautogui.press('enter')
    submit = browser.find_elements_by_xpath('//*[@name="submit"]')
    submit[0].click()
    print('[',tiemcounter,'] Detective gehuurd voor:', tiem[0])
    tiemcounter = tiemcounter + 1
