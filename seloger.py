import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from fake_useragent import UserAgent
import csv




driver_path = r"C:\Users\admin\Desktop\chromedriver.exe"


# SETTINGS
url = "https://www.seloger.com/list.htm?tri=initial&enterprise=0&idtypebien=2,1&idtt=2,5&naturebien=1,2,4&cp=75&m=search_hp_new"



chrome_options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
chrome_options.add_argument(f'user-agent={userAgent}')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--log-level=3')
browser = webdriver.Chrome(driver_path, options=chrome_options)
browser.set_script_timeout(5)
browser.get(url)

html = browser.page_source
soup = BeautifulSoup(html, 'lxml')

print(soup)
input("......")


# CREATE CSV FILE SAME DIRECTORY
with open('selegor_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['price', 'title', 'tags', 'address'])

   

file.close()
# INFO
print("------------------------------------------------")
print("End")  
print("------------------------------------------------")
        
