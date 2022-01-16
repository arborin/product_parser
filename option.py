import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# SETTINGS
url = "https://optionstrat.com/build/long-call/TSLA/220128C1055"
driver_path = r"C:\Users\admin\Desktop\chromedriver.exe"


chrome_options = Options()

chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')




browser = webdriver.Chrome(driver_path, options=chrome_options)
browser.set_script_timeout(10)
browser.get(url)


wait = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.swiper-slide')))

html = browser.page_source
soup = BeautifulSoup(html, 'lxml')



target_div =  soup.find("div", class_="swiper-slide swiper-slide-active")

# print(target_div)

all_sections = target_div.find_all("div", class_="StrategyStatsPanel_section__3SVBL")

for section in all_sections:
    all_spans = section.find_all("span")
    print(all_spans[0].text)
    print(all_spans[-1].text)
    print("----------------------------------")
# input("......")












