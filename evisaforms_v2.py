import time
import datetime
import smtplib
import schedule
import json
import requests
import argparse
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


class Visa:

    def __init__(self, url, radio, color, integromat_url):
        self.url = url
        self.radio = radio
        self.color = f'#{color}'
        self.integromat_url = integromat_url

        self.browser_config()


    def send_mail_request(self):
        response = requests.post(url)
        return response


    def browser_config(self):
        
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
        self.driver = webdriver.Chrome(options=options)

        # FOR TESTING 
        #alert_color = "#ADD9F4" 

        # YELLO COLOR / UNCOMMENT THIS
        # alert_color = "#ffffc0";
        
        

    def run_task(self):
        self.driver.get(self.url)
        time.sleep(5)

        # GET FIRST INPUT FROM PAGE AND CLICK
        buttons = self.driver.find_element_by_tag_name("input").click()
        time.sleep(5)

        # CLICK TO SECOND RADIOBOX
        self.driver.find_element_by_xpath(f"//input[@value='{self.radio}']").click()
        time.sleep(1)

        # CLICK CHECKBOX
        self.driver.find_element_by_xpath("//input[@name='chkbox01']").click()
        time.sleep(1)

        # CLICK SUBMIT
        self.driver.find_element_by_xpath("//input[@type='submit']").click()

        # GET PAGE CONTENT
        html = self.driver.page_source
        time.sleep(2)


        # GO TO NEXT MONTH
        month_select = Select(self.driver.find_element_by_id('Select1'))
        year_select =  Select(self.driver.find_element_by_id('Select2'))


        cur_month = datetime.datetime.now().month
        cur_year = datetime.datetime.now().month
        if cur_month < 12:
            next_month = str(cur_month + 1)
            #  SELECT NEXT MONTH 
            month_select.select_by_value(next_month)
            
        else:
            # IF IT IS DECEMBER=12, NEXT MONTH WILL BE JANUARY=1
            next_month = "1"
            next_year = str(cur_year + 1)
            # SELECT NEXT YEAR FIRST MONTH
            year_select.select_by_value(next_year)
            month_select.select_by_value(next_month)

        next_month_html = self.driver.page_source

        self.driver.quit()

        # SOUP HTML CONTENT
        soup = BeautifulSoup(html, 'lxml')
        next_month_soup = BeautifulSoup(next_month_html, 'lxml')

        # GET CALENDAR TABLE
        calendar_table = soup.find("table", id='Table3')
        next_calendar_table = next_month_soup.find("table", id='Table3')

        # FIND ALL DAYS WHICH HAS TARGET ALERT COLOR
        # COLOR MAY BE #ffffc0 OR #FFFFC0
        alert_day_low = calendar_table.find_all("td", attrs={'bgcolor': self.color.lower()})
        alert_day_up = calendar_table.find_all("td", attrs={'bgcolor': self.color.upper()})

        next_alert_day_low = next_calendar_table.find_all("td", attrs={'bgcolor': self.color.lower()})
        next_alert_day_up = next_calendar_table.find_all("td", attrs={'bgcolor': self.color.upper()})


        # IF FIND ANY APPOINTMENT DAYS (IN CURRENT MONTH OR IN THE NEXT MONTH), SEND REQUEST
        if (
            len(alert_day_low)>0 or len(alert_day_up)>0 or
            len(next_alert_day_low)>0 or len(next_alert_day_up)>0
            ):
            
            # CALL integromat REQUEST SENDER FUNCTION
            self.send_mail_request()
            
            print('[INFO] - Alert color found, Mail Sent')  
        else:
            print("[INFO] - Alert color not found")

        




if __name__ == "__main__":
    
    # url = "https://evisaforms.state.gov/acs/default.asp?postcode=LND&appcode=1"
    # radio = "02B"
    # color = "#ADD9F4"
    # integromat_url = "https://hook.integromat.com/mpad48u26x4cghg222uq9x6774727wmt"


    parser = argparse.ArgumentParser(prog='parsePlotSens');
    parser.add_argument('--url', required=True, help="Target page url")
    parser.add_argument('--radio', required=True, help="Apache log type [Passport services, Report the birth abroad, Request notarial]")
    parser.add_argument('--color', required=True, choices=['ADD9F4', 'ffffc0'], help="Calendar day colors [BLUE, YELLOW]")
    parser.add_argument('--integromat', required=True, help="Integromat url")
    
    option = parser.parse_args()
    

    # GET CLI ARGUMENTS
    url = option.url
    radio = option.radio
    color = option.color
    integromat_url = option.integromat

      
    # CREATE CLASS OBJECT AND RUN TASK
    scrap = Visa(url, radio, color, integromat_url)
    scrap.run_task()



# USE THIS COMMAND TU RUN SCRIPT 

# python3 evisaforms_v2.py --url https://evisaforms.state.gov/acs/default.asp?postcode=LND --radio 02B --color ADD9F4 --integromat https://hook.integromat.com/mpad48u26x4cghg222uq9x6774727wmt



