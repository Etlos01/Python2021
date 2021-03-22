from selenium import webdriver
import bs4
import json
import requests
import re
import regex
import datetime
import pandas as pd

from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Webscraper:

    def __init__(self, url):
        self.url = url
        self.cards = []

    
    def search(self, param):
        options = Options()
        options.headless = True
        print("Initialzin webdriver")
        start = datetime.datetime.now()
        browser = webdriver.Firefox(options=options)

        print('Lets go!')
        print("Fetching url")
        browser.get(self.url)
        print("Telling browser to wait 2 sec by deault")
        browser.implicitly_wait(2)
        
        print("Rejecting cookies")
        browser.find_elements_by_tag_name('button')[1].click()
        browser.implicitly_wait(2)
        
        print("Finding Nvidea cards")
        browser.find_elements_by_class_name('_2Jn2-PLos3')[0].click()
        browser.implicitly_wait(10)
        
        print("Consulting the 'most popular searches' div to find the most popular processor")
        browser.find_elements_by_class_name('_3kbvwJ4edH')[0].click()
        
        string_url = browser.current_url
        print('Seems like the most popular card is: ' + string_url)
        req = requests.get(string_url)
        soup = bs4.BeautifulSoup(req.text, 'html.parser')
        mydivs = soup.find_all("div", {"class": "_2Vdwcz_zWR _1bgVr-M90D"})
        cards_column = []
        price_column = []
        for card in mydivs:
            cards_column.append(card.find("div", {"class" : "_3jyYcmGfmy"}).get('title', 'No title found'))
            price_column.append(card.select_one('span[class*="_1hXG0xPrK5 _3GiEsJk2wF"]').text.strip('fra'))
        self.cards = pd.DataFrame(data={'Graphics Cards': cards_column, 'Price': price_column})
        finish = datetime.datetime.now()
        print(finish - start)
        browser.quit()