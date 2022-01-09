from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# FOR TESTING
begin_time = datetime.datetime.now()


#=====================================================================================
# CONFIGURATION
#=====================================================================================

# TARGET URL ADDRESS
url = "https://evisaforms.state.gov/acs/default.asp?postcode=LND&appcode=1"

# FOR TESTING 
alert_color = "#ADD9F4" 

# YELLO COLOR / UNCOMMENT THIS
# alert_color = "#ffffc0";

# EMAIL SETTINGS 
mail_content = '''Email Text On alert'''
sender_address = 'developmentmail36@gmail.com'
sender_pass = 'c831385ef5eec6'
receiver_address = 'nika.kobaidze@gmail.com'
subject = "Alert"


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
driver = webdriver.Chrome(r"C:\Users\admin\Desktop\chromedriver.exe", options=options)

#=====================================================================================
# END CONFIGURATION
#=====================================================================================


#=====================================================================================
# START SCRIPT
#=====================================================================================

# OPEN URL
driver.get(url)
time.sleep(5)

# GET FIRST INPUT FROM PAGE AND CLICK
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

# CLOSE BROWSER
driver.quit()

# SOUP HTML CONTENT
soup = BeautifulSoup(html, 'lxml')

# GET CALENDAR TABLE
calendar_table = soup.find("table", id='Table3')

# FIND ALL DAYS WHICH HAS TARGET ALERT COLOR
# COLOR MAY BE #ffffc0 OR #FFFFC0
alert_day_low = calendar_table.find_all("td", attrs={'bgcolor': alert_color.lower()})
alert_day_up = calendar_table.find_all("td", attrs={'bgcolor': alert_color.upper()})


# IF FIND ANY DAY SEND EMAIL
if len(alert_day_low)>0 or len(alert_day_up)>0:
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

    print('Alert color found, Mail Sent')
else:
    print("Alert color not found")


print("============================================")
print("Script run time")
print(datetime.datetime.now() - begin_time)
print("============================================")