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

print(country_select)

# options = [x for x in country_select.find_elements_by_tag_name("option")]
# this part is cool, because it searches the elements contained inside of select_box 
# and then adds them to the list options if they have the tag name "options"

for option in country_select.options:
    country = option.text
    value = option.get_attribute('value')

    print("COUNTRY: {} / CODE: {}".format(country, value))

    country_select.select_by_value(value)

    time.sleep(2)
    city_select = Select(driver.find_element(By.NAME, 'PostCodeShow'))

    for city in city_select.options:
        print(city.text)
    
    time.sleep(2)

    
 





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
