import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time


# SETTINGS
url = "http://www.exteriores.gob.es/Consulados/LONDRES/es/ServiciosConsulares/Paginas/respingo.aspx"

driver_path = r"C:\Users\User\Desktop\chromedriver.exe"


# SET OPTIONS
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')


#
browser = webdriver.Chrome(driver_path, options=chrome_options)
browser.implicitly_wait(10)


# OPEN PAGE
browser.get(url)


# FIND <a> ELEMENT BY TEXT
elem = browser.find_element_by_link_text("ENLACE")


# THERE IS A 4 ELEMENT WITH NAME "ENLACE"
# SECOND ONE IS A TARGET
enlance_links = browser.find_elements(By.XPATH, '//a[text()="ENLACE"]')


# CLICK ON THAT LINK
enlance_links[1].click()

time.sleep(10)


# GO TO ACTIVE TAB TO GET ITS CONTENT
browser.switch_to.window(browser.window_handles[-1])


# GET HTML CONTENT
html = browser.page_source


# USE html.parser (WORKED BETTER THEN lxml)
soup = BeautifulSoup(html, 'html.parser')


# FIND TARGET DIV
div_content = soup.find('div', attrs={'id':"idDivNotAvailableSlotsTextTop"})


if div_content:
    div_text = div_content.text.strip()
    if div_text == "No hay horas disponibles":
        print(div_text)
else:
    print("FIND SOME OTHER CONTENT SEND ALERT REQUEST")
