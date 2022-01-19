import time
import datetime
import smtplib
import schedule
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
import json
import requests



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
webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

# CHANGE CHROMEDRIVER PATH
driver = webdriver.Chrome(options=options)


#=====================================================================================
# END CONFIGURATION
#=====================================================================================

driver.get(url)
time.sleep(5)

# GET FIRST INPUT FROM PAGE AND CLICK



# GO TO NEXT MONTH
country_select = Select(driver.find_element(By.NAME, 'CountryCodeShow'))



# options = [x for x in country_select.find_elements_by_tag_name("option")]
# this part is cool, because it searches the elements contained inside of select_box 
# and then adds them to the list options if they have the tag name "options"
country_data = []

# country={'country': "", "code":"", "city":[{"city": "", "code": ""}]}




for option in country_select.options[1:2]:

    country_dict = {}
    country = option.text
    value = option.get_attribute('value')

    country_dict['country'] = country.strip()
    country_dict['code'] = value.strip()

    # print("COUNTRY: {} / CODE: {}".format(country, value))

    country_select.select_by_value(value)

    time.sleep(0.1)
    city_select = Select(driver.find_element(By.NAME, 'PostCodeShow'))

    city_list = []
    for city_option in city_select.options[1:]:
        city = {}
        city['city_name'] = city_option.text.strip()
        city['code'] = city_option.get_attribute('value').strip()

        city_list.append(city)
    

    country_dict['city'] = city_list

        # city_select.select_by_value(value)

        # # CLICK SUBMIT BUTTON
        # driver.find_element_by_xpath("//input[@type='submit']").click()

        # # CLICK MAKE APPOINTMENT BTN
        # buttons = driver.find_element_by_tag_name("input").click()
        # time.sleep(5)

        
        
        # GET OPTION CODES AND VALUES
    country_data.append(country_dict)



for country in country_data:

    base_url = "https://evisaforms.state.gov/acs/default.asp?postcode="

    for city in country['city']:
        city_code = city['code']

        city_url = base_url+city_code

        driver.get(city_url)

        # CLICK BUTTON
        buttons = driver.find_element_by_tag_name("input").click()
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
            name = address_line[1].strip()
            address = ("").join(address_line[2:]).strip()
        
        print("\n\n\n")
        print(city['city_name'])
        print(city_code)
        print(city_url)
        print(name)
        print(address)



        # GET CALENDAR TABLE
        option_table = soup.find("table", {'class':'htframe'})
        # print(option_table)
        
        trs = option_table.find_all("tr")



        for tr in trs:
            # GET RADIO VALUE
            radio = tr.find("input")
            radio_value = ''
            radio_text = ''

            if radio:
                radio_value = radio['value']
            
            # GET TEXT
            text_val = tr.find("td",{'class': 'formfield'})
            if text_val:
                radio_text = text_val.text

            if radio_value and radio_text:
                print(f"{radio_value} --- {radio_text}")

            
            print("---------------------------------------------")

        



    
 





# else:
# # IF IT IS DECEMBER=12, NEXT MONTH WILL BE JANUARY=1
# next_month = "1"
# next_year = str(cur_year + 1)
# # SELECT NEXT YEAR FIRST MONTH
# year_select.select_by_value(next_year)
# month_select.select_by_value(next_month)

# next_month_html = driver.page_source


# driver.quit()

# except:
# # CLOSE BROWSER
# driver.quit()
# print("[ERROR] - {} - Something went wrong".format(curtime))

# else:
# # SOUP HTML CONTENT
# soup = BeautifulSoup(html, 'lxml')
# next_month_soup = BeautifulSoup(next_month_html, 'lxml')

# # GET CALENDAR TABLE
# calendar_table = soup.find("table", id='Table3')
# next_calendar_table = next_month_soup.find("table", id='Table3')

# # FIND ALL DAYS WHICH HAS TARGET ALERT COLOR
# # COLOR MAY BE #ffffc0 OR #FFFFC0
# alert_day_low = calendar_table.find_all("td", attrs={'bgcolor': alert_color.lower()})
# alert_day_up = calendar_table.find_all("td", attrs={'bgcolor': alert_color.upper()})

# next_alert_day_low = next_calendar_table.find_all("td", attrs={'bgcolor': alert_color.lower()})
# next_alert_day_up = next_calendar_table.find_all("td", attrs={'bgcolor': alert_color.upper()})


# # IF FIND ANY APPOINTMENT DAYS (IN CURRENT MONTH OR IN THE NEXT MONTH), SEND REQUEST
# if (
# len(alert_day_low)>0 or len(alert_day_up)>0 or
# len(next_alert_day_low)>0 or len(next_alert_day_up)>0
# ):

# if get_send_status():
#     # CALL integromat REQUEST SENDER FUNCTION
#     send_mail_request("nika.kobaidze@gmail.com", "Mail text")
    
#     # DISABLE REQUEST SENDING
#     set_send_status(0)

#     print('[INFO] - {} - Mail Sent'.format(curtime))
    
# else:
#     print('[INFO] - {} - Disable Mail Sending...'.format(curtime))
# else:
# # IF DATE NOT FOUND ENABLE SEND MAIL
# set_send_status(1)

# print("[INFO] - {} - Alert color not found".format(curtime))

# print("[INFO] - {} - Script run time {}".format(curtime, datetime.datetime.now() - begin_time))


# # job()
# schedule.every(1).minutes.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)



