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

print("All modules loaded")

# RESET DATA WHEN SCRIPT RUNS FIRST
# file = open('data.json', 'w');



def set_send_status(status):
    json_data = {"send_mail": status}
    with open('data.json', 'w') as fp:    
        json.dump(json_data, fp)

def get_send_status():
    with open('data.json', 'r') as fp:    
        data = json.load(fp)
    return data['send_mail']


# SET SEND STATYS ENABLE BY DEFAULT
set_send_status(1)


def job():
    #=====================================================================================
    # CONFIGURATION
    #=====================================================================================
    curtime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("[INFO] - {} - script is running...".format(curtime))
    # TARGET URL ADDRESS
    url = "https://evisaforms.state.gov/acs/default.asp?postcode=LND&appcode=1"

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

    # FOR TESTING 
    alert_color = "#ADD9F4" 

    # YELLO COLOR / UNCOMMENT THIS
    # alert_color = "#ffffc0";
    
   
    #=====================================================================================
    # END CONFIGURATION
    #=====================================================================================
    
    # FOR TESTING
    begin_time = datetime.datetime.now()
    # OPEN URL
    driver.get(url)
    time.sleep(5)

    # GET FIRST INPUT FROM PAGE AND CLICK
    try:
        buttons = driver.find_element_by_tag_name("input").click()
        time.sleep(5)

        # CLICK TO SECOND RADIOBOX
        driver.find_element_by_xpath("//input[@value='02B']").click()
        time.sleep(1)

        # CLICK CHECKBOX
        driver.find_element_by_xpath("//input[@name='chkbox01']").click()
        time.sleep(1)

        # CLICK SUBMIT
        driver.find_element_by_xpath("//input[@type='submit']").click()

        # GET PAGE CONTENT
        html = driver.page_source
        time.sleep(2)
        # GO TO NEXT MONTH
        month_select = Select(driver.find_element_by_id('Select1'))
        year_select =  Select(driver.find_element_by_id('Select2'))


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

        next_month_html = driver.page_source
        
        
        # print(next_month_html)
        # input("test")
        # CLOSE BROWSER
        driver.quit()

    except:
        # CLOSE BROWSER
        driver.quit()
        print("[ERROR] - {} - Something went wrong".format(curtime))

    else:
        # SOUP HTML CONTENT
        soup = BeautifulSoup(html, 'lxml')
        next_month_soup = BeautifulSoup(next_month_html, 'lxml')

        # GET CALENDAR TABLE
        calendar_table = soup.find("table", id='Table3')
        next_calendar_table = next_month_soup.find("table", id='Table3')

        # FIND ALL DAYS WHICH HAS TARGET ALERT COLOR
        # COLOR MAY BE #ffffc0 OR #FFFFC0
        alert_day_low = calendar_table.find_all("td", attrs={'bgcolor': alert_color.lower()})
        alert_day_up = calendar_table.find_all("td", attrs={'bgcolor': alert_color.upper()})

        next_alert_day_low = next_calendar_table.find_all("td", attrs={'bgcolor': alert_color.lower()})
        next_alert_day_up = next_calendar_table.find_all("td", attrs={'bgcolor': alert_color.upper()})


        
        # IF FIND ANY DAY SEND EMAIL
        if (
            len(alert_day_low)>0 or len(alert_day_up)>0 or
            len(next_alert_day_low)>0 or len(next_alert_day_up)>0
            ):

            # EMAIL SETTINGS
            # PLEASE CHANGE EMAIL ADDRESSES
            if get_send_status():
                mail_content = '''Email Text On alert'''
                sender_address = 'developmentmail36@gmail.com'
                sender_pass = 'c831385ef5eec6'
                receiver_address = 'nika.kobaidze@gmail.com'
                subject = "Alert"
                #Setup the MIME
                message = MIMEMultipart()
                message['From'] = sender_address
                message['To'] = receiver_address
                message['Subject'] = subject 
                message.attach(MIMEText(mail_content, 'plain'))
                #Create SMTP session for sending the mail
                session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
                session.starttls() #enable security
                session.login(sender_address, sender_pass) #login with mail_id and password
                text = message.as_string()
                session.sendmail(sender_address, receiver_address, text)
                session.quit()

                # SEND EMAIL AND DISABLE MAIL SENDING
                set_send_status(0)

                print('[INFO] - {} - Mail Sent'.format(curtime))
            else:
                print('[INFO] - {} - Disable Mail Sending...'.format(curtime))
        else:
            # IF DATE NOT FOUND ENABLE SEND MAIL
            set_send_status(1)
            
            print("[INFO] - {} - Alert color not found".format(curtime))

            print("[INFO] - {} - Script run time {}".format(curtime, datetime.datetime.now() - begin_time))
  	

# job()
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
