# SETUP
# 1. INSTALL selenium  
# pip install -U selenium

# 2. INSTALL BeautifulSoup 
# pip install bs4

# 3. INSTALL lxml library 
# pip install lxml

# 4. DOWNLOAD CHROME DRIVER: 
# https://chromedriver.storage.googleapis.com/index.html?path=96.0.4664.45/
# browser = webdriver.Chrome(r"FULL_PATH_OF_WEBDRIVER.EXE")


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import csv



# !!! CHANGE THIS PATH WITH YOUR chromedriver LOCATION !!! 
driver_path = r"C:\Users\admin\Desktop\chromedriver.exe"

# TARGET URL
url = "https://www.apps.akc.org/apps/fastcat_ranking/"

# CSV
csv_file = "fastcat_ranking.csv"


chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--log-level=3')
browser = webdriver.Chrome(driver_path, options=chrome_options)
browser.set_script_timeout(5)
browser.get(url)

html = browser.page_source
soup = BeautifulSoup(html, 'lxml')


# GET year OPTIONS
years = soup.find('select', id="in_year")
year_options = years.find_all('option') # REMOVE LAST ELEMENT "lifetime"


# GET breed OPTIONS
breeds = soup.find('select', id="in_cde_bvg_num")
breeds_options = breeds.find_all('option')[1:] # REMOVE FIRST ELEMENT "Select A Bread"


# RECORD COUNTER
counter = 0 


with open(csv_file, 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(['entry_id', 'year', 'breed', 'rank', 'dog_name', 'gender','speed'])

    # CHECKS BREED BY YEAR
    for breed in breeds_options:
        breed_val = breed['value']
        breed_text = breed.text
                
        # SELECT BREED
        select_bread = Select(browser.find_element_by_id('in_cde_bvg_num'))
        select_bread.select_by_value(breed_val)
        
        for year in year_options:
            year_val = year['value']
            year_text = year.text

            # SELECT YEAR
            select_year = Select(browser.find_element_by_id('in_year'))
            select_year.select_by_value(year_val)

            # CLICK SEARCH BTN
            search_result = browser.find_element_by_xpath('//button[text()="Get Rankings"]').click()
            # TIMEOUT 
            browser.set_script_timeout(5)

            html = browser.page_source
            soup = BeautifulSoup(html, 'lxml')
            
            # CHECK INF RECORDS EXISTS
            try:
                table = soup.find("table", {'class': "etrTable"})
                tbody = table.find('tbody')

                rows = tbody.find_all("tr")[1:] # REMOVE TABLE TITLE ROW
                for row in rows:
                    counter+=1

                    cols = row.find_all('td')
                    
                    rank = cols[0].text.strip().replace('\n', '').replace('\t','')
                    dog_name = cols[1].text.strip().replace('\n', '').replace('\t','')
                    gender = cols[2].text.strip().replace('\n', '').replace('\t','')
                    speed = cols[3].text.strip().replace('\n', '').replace('\t','')

                    text_col = [counter, year_text, breed_text, rank, dog_name, gender, speed]

                    writer.writerow(text_col)
                    print(text_col)
                    print("=======================================================")
            except:
                print("Record not found")
    
    
    
        


















# for row in all_rows:
#     print(row)


# CREATE USER 'pda'@'localhost' IDENTIFIED WITH mysql_native_password BY 'pda';


# select = Select(driver.find_element_by_id('fruits01'))

# # select by visible text
# select.select_by_visible_text('Banana')

# # select by value 
# select.select_by_value('1')