import time
import datetime
import smtplib
import schedule
import csv
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




print("All modules loaded")



#=====================================================================================
# CONFIGURATION
#=====================================================================================

# TARGET URL ADDRESS
url = "https://evisaforms.state.gov/Instructions/ACSSchedulingSystem.asp#top"

# BROWSER OPTIONS
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--start-maximized')
# options.add_argument('--start-fullscreen')
options.add_argument('--single-process')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--incognito")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("disable-infobars")
options.add_argument('--log-level=3')

webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

# CHANGE CHROMEDRIVER PATH
driver = webdriver.Chrome(options=options, service_log_path='/dev/null')


#=====================================================================================
# END CONFIGURATION
#=====================================================================================

driver.get(url)
time.sleep(5)

# GET FIRST INPUT FROM PAGE AND CLICK



# GO TO NEXT MONTH
country_select = Select(driver.find_element(By.NAME, 'CountryCodeShow'))

country_data = []

# EXAMPLE TEMPLATE DICT
# country={'country': "", "code":"", "city":[{"city": "", "code": ""}]}


for option in country_select.options[1:]:

    country_dict = {}
    country = option.text
    value = option.get_attribute('value')

    # STRIP TEXT
    country_dict['country'] = country.strip()
    country_dict['code'] = value.strip()

    # print("COUNTRY: {} / CODE: {}".format(country, value))

    # SELECT COUTRY WITH VALUE
    country_select.select_by_value(value)
    time.sleep(0.1)

    # GET ALL CITY VALUES
    city_select = Select(driver.find_element(By.NAME, 'PostCodeShow'))

    city_list = []
    for city_option in city_select.options[1:]:
        city = {}
        city['city_name'] = city_option.text.strip()
        city['code'] = city_option.get_attribute('value').strip()

        city_list.append(city)
    

    country_dict['city'] = city_list
   
    # GET OPTION CODES AND VALUES
    country_data.append(country_dict)



with open("collect_options.csv", 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    # MAY BE TITLES WRITTEN FOR EACH COLUMN
    # writer.writerow(['Title1', 'Title1', 'Title1', 'Title1', 'Title1', 'Title1','Title1'])

    for country in country_data:
        try:
            country_name = country['country']

            base_url = "https://evisaforms.state.gov/acs/default.asp?postcode={}&appcode=1"

            for city in country['city']:
                city_code = city['code']
                city_name = city['city_name']

                city_url = base_url.format(city_code)

                driver.get(city_url)

                # CLICK BUTTON
                time.sleep(5)
                buttons = driver.find_element(By.TAG_NAME, "input").click()
                time.sleep(5)

                # GET OPTIONS
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')


                # GET TITLE AND ADDRESS
                title_table = soup.find("table")
                title_trs = title_table.find_all("tr")
                title_td = title_trs[2].find("td")
                
                if title_td:
                    address_line = title_td.text.split('\n')
                    embassy_name = address_line[1].strip().replace(',','')
                    embassy_address = ("").join(address_line[2:]).strip().replace(',','')
                
                
                # GET TABLE
                option_table = soup.find("table", {'class':'htframe'})
                # print(option_table)
                
                trs = option_table.find_all("tr")

                for tr in trs:
                    # GET RADIO VALUE FOR EACH TABLE ROW
                    radio = tr.find("input")
                    radio_value = ''
                    radio_text = ''

                    # GET RADIO BUTTON VALUE
                    if radio:
                        radio_value = radio['value']
                    
                    # GET RADIO BUTTON TEXT
                    text_val = tr.find("td",{'class': 'formfield'})
                    if text_val:
                        radio_text = text_val.text.replace(',','')


                    if radio_value and radio_text:
                        print("---------------------------------------------------------------------------------------")
                        csv_str = f"{country_name},{embassy_name},{radio_text},{radio_value},{city_url},{city_code},{embassy_address}"
                        print(csv_str)

                        # WRITE INTO CSV
                        writer.writerow([country_name, embassy_name, radio_text, radio_value, city_url, city_code, embassy_address])
        except:
            print("ERROR")
            csv_str = f"ERROR ON: {country['country']}"