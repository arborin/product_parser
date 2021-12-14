
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv


# SETTINGS
url = "https://www.notariato.it/it/trova-notaio/"
# driver_path = r"C:\Users\Administrator\Documents\nika_kobaidze\scripts\chromedriver.exe"
driver_path = r"C:\Users\admin\Desktop\chromedriver.exe"



chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--log-level=3')
browser = webdriver.Chrome(driver_path, options=chrome_options)

browser.get(url)

search = browser.find_element_by_xpath("//button[@type='submit']").click()

# print(search)

html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
# # GETING ALL "article" TAGS 
cards = soup.find_all('div', class_="bottone")

for card in cards:
    print(card.a['href'])

