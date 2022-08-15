import time
from selenium import webdriver
from selenium.webdriver.common import keys
import pyautogui
import keyboard
from bs4 import BeautifulSoup
import requests
import lxml
from datetime import datetime
import re
import random
from config import mw_username, mw_password, mw_findladies, mw_keepcars, mw_sellcar, mw_geldstorten, mw_geldstorten_als, mw_geldstoren_houden, mw_boksen, mw_random

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")

globalfindladies = datetime.now().replace(microsecond=0)
browser = webdriver.Chrome(chrome_options=options)

globalcarpause = 0
totalloot = 0

loginurl = 'http://www.maffiaweaks.nl/login'
list1_url = []
payload = {
    'username': mw_username,
    'password': mw_password,
    'submit': 'Inloggen'
}

def tijd():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_timetime = ' [' + current_time + '] '
    return current_timetime

def anticaptcha():
    gunlocation = pyautogui.locateOnScreen('gun2.png', region=(850, 550, 300, 600), grayscale=True, confidence=0.8)
    if gunlocation is not None:
        gunpoint = pyautogui.center(gunlocation)
        gunx, guny = gunpoint
        pyautogui.click(gunx, guny)

def mwlogin():
    browser.get('http://www.maffiaweaks.nl/login')
    browser.set_window_size(1024, 600)
    browser.maximize_window()
    loginbalk = browser.find_elements_by_xpath('//*[@type="text"]')
    loginbalk[1].click()
    pyautogui.write(mw_username, interval=0.05)
    loginpass = browser.find_elements_by_xpath('//*[@type="password"]')
    loginpass[1].click()
    pyautogui.write(mw_password, interval=0.05)
    pyautogui.press('enter')
    print(tijd(), 'Succesfully logged in')

def dotnum(a):
    numberstr = str(a)
    fixed = (re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', numberstr))
    return fixed

def do_crime():
    try:
        if not keyboard.is_pressed('q'):
            browser.get('http://www.maffiaweaks.nl/prison/pay/' + mw_username)
            browser.get('http://www.maffiaweaks.nl/crimes')
            time.sleep(1)
            buttons = browser.find_elements_by_xpath('//*[@type="radio"]')
            buttons[8].click()
            anticaptcha()
            if mw_random.lower() == 'yes':
                time.sleep(random.randint(15, 18))
        else:
            input(tijd(), 'Druk enter om verder te gaan')
            do_crime()
    except IndexError:
        print(tijd(), 'Crime index error')

def do_car():
    try:
        if not keyboard.is_pressed('q'):
            global globalcarpause
            browser.get('http://www.maffiaweaks.nl/prison/pay/' + mw_username)
            browser.get('http://www.maffiaweaks.nl/cars/steal')
            time.sleep(1)
            buttons = browser.find_elements_by_xpath('//*[@type="radio"]')
            buttons[0].click()
            anticaptcha()
            globalcarpause += 1
            print(tijd(), 'Rotation [', globalcarpause, '] done.')
            if mw_random.lower() == 'yes':
                time.sleep(random.randint(1, 3))
        else:
            input(tijd(), 'Druk enter om verder te gaan')
            do_car()
    except IndexError:
        print(tijd(), 'Car index error')

def sellcar():
    global globalcarpause
    globalcarpause += 1
    browser.get('http://www.maffiaweaks.nl/prison/pay/' + mw_username)
    carcount = 0
    keep_car_list = []
    with requests.session() as s:
        s.post(loginurl, data=payload)
        r = s.get('http://www.maffiaweaks.nl/cars')
        soup = BeautifulSoup(r.content, 'lxml')
        find_tables = soup.find_all('table', class_='wrap_table')
        del find_tables[0]
        for item in find_tables:
            deeper = item.find_all('td', class_='tsub')
            if deeper[1].text in mw_keepcars:
                keep_car_list.append(carcount)
                carcount += 1
            else:
                carcount += 1
            if len(deeper) == 4:
                if deeper[3].text in mw_keepcars:
                    keep_car_list.append(carcount)
                    carcount += 1
                else:
                    carcount += 1
        browser.get('http://www.maffiaweaks.nl/cars')
        time.sleep(1)
        sellb = browser.find_elements_by_xpath('//*[@type="checkbox"]')
        if len(sellb) > 1 + len(keep_car_list):
            sellb[-1].click()
            for item in keep_car_list:
                sellb[item].click()
            honka = browser.find_elements_by_xpath('//*[@href="cars/dealer"]')
            honka[-1].click()

            booba = browser.find_elements_by_xpath('//*[@name="confirm"][@value="Ja"]')
            booba[0].click()
            print(tijd(), 'sold cars')
            if mw_random.lower() == 'yes':
                time.sleep(random.randint(1, 3))

        else:
            print(tijd(), 'no cars to sell')

def cashcheck():
    global totalloot
    browser.get('http://www.maffiaweaks.nl/prison/pay/' + mw_username)
    with requests.session() as s:
        s.post(loginurl, data=payload)
        r = s.get('http://www.maffiaweaks.nl/bank')
        soup = BeautifulSoup(r.content, 'lxml')
        find_table = soup.find_all('table', class_='content_table')
        found = find_table[1].find_all('td', class_='tcell')
        cashamount = found[5].text.replace(' ', '').replace('€', '').replace('.', '')
        cashamount = int(cashamount)
        if cashamount > mw_geldstorten_als:
            browser.get('http://www.maffiaweaks.nl/bank')
            time.sleep(1)
            finddepo = browser.find_elements_by_xpath('//*[@name="amount"]')
            finddepo[0].click()
            cashamount = cashamount - mw_geldstoren_houden
            totalloot = totalloot + cashamount
            cashamount = str(cashamount)
            pyautogui.write(cashamount)
            pyautogui.press('enter')
            print(tijd(), 'Deposited ', dotnum(cashamount))
            if mw_random.lower() == 'yes':
                time.sleep(random.randint(1, 3))

def findladies():
    browser.get('http://www.maffiaweaks.nl/prison/pay/' + mw_username)
    browser.get('http://www.maffiaweaks.nl/red-light-district/search')
    time.sleep(1)
    anticaptcha()
    print(tijd(), 'Kechies complete')
    if mw_random.lower() == 'yes':
        time.sleep(random.randint(1, 3))

def boxen():
    browser.get('http://www.maffiaweaks.nl/prison/pay/' + mw_username)
    browser.get('http://www.maffiaweaks.nl/boxing')
    time.sleep(1)
    anticaptcha()
    print(tijd(), 'boksen complete')
    if mw_random.lower() == 'yes':
        time.sleep(random.randint(1, 3))

def gokken():
    creditsingezet = 0
    creditsgewonnen = 0
    browser.get('http://www.maffiaweaks.nl/slots')
    inzetbox = browser.find_elements_by_xpath('//*[@name="inzet"]')
    inzetbox[0].click()
    pyautogui.press('backspace')
    pyautogui.write('50')
    spelenbox = browser.find_elements_by_xpath('//*[@value="SPELEN"]')
    while True:
        spelenbox[0].click()
        creditsingezet += 50
        time.sleep(2.5)
        while True:
            gokkenresult = browser.find_elements_by_xpath('//*[@id="info"]')
            tttt = gokkenresult[0].text
            if tttt != ' ':
                print(tijd(), tttt)
                break

def configcheck():
    if mw_geldstorten.lower() == 'yes':
        cashcheck()
    if mw_findladies.lower() == 'yes':
        findladies()
    if mw_sellcar.lower() == 'yes':
        sellcar()
    if mw_boksen.lower() == 'yes':
        boxen()

startingtime = datetime.now().replace(microsecond=0)
rotationtimer = datetime.now().replace(microsecond=0)

mwlogin()

if mw_sellcar.lower() == 'yes':
    sellcar()

while True:
    for y in range(0, 5):
        for x in range(0, 4):
            do_crime()
        do_car()

    configcheck()
    print(tijd(), 'Loot: ', dotnum(totalloot), 'timer: ', datetime.now().replace(microsecond=0) - startingtime, 'rotation: ', datetime.now().replace(microsecond=0) - rotationtimer)
    rotationtimer = datetime.now().replace(microsecond=0)
