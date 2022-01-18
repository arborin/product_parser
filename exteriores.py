import requests
import time
import schedule
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


print("All modules loaded")


def set_send_status(status):
    json_data = {"send_mail": status}
    
    with open('script_data.json', 'w') as fp:    
        json.dump(json_data, fp)


def get_send_status():
    with open('script_data.json', 'r') as fp:    
        data = json.load(fp)
    return data['send_mail']



def send_mail_request(email_address, message):
    # WEBHOOK URL
    url = "https://hook.integromat.com/mpad48u26x4cghg222uq9x6774727wmt"
    # WEBHOOK PARAMETERS
    post_data = {'email_address': email_address, 'message': message}
    # SEND POST REQUEST
    response = False

    try:
        response = requests.post(url, data = post_data)
    except Exception as e:
        print("REQUEST SEND ERROR: {}".format(e)) 

    return response



# RESET DATA WHEN SCRIPT RUNS FIRST
# SET SEND STATYS ENABLE BY DEFAULT
set_send_status(1)



def job():
    # SETTINGS
    url = "http://www.exteriores.gob.es/Consulados/LONDRES/es/ServiciosConsulares/Paginas/respingo.aspx"

    # WILL CHECK NECT 10 DAYS
    day_range = 10

    # FOR WINDOWS
    # driver_path = r"C:\Users\User\Desktop\chromedriver.exe"


    # SET OPTIONS
    chrome_options = Options()
    chrome_options.add_argument('--log-level=3')


    # FOR WINDOWS
    # browser = webdriver.Chrome(driver_path, options=chrome_options)

    browser = webdriver.Chrome(options=chrome_options)
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
    next_day = browser.find_element(By.ID, "idDivBktDatetimeSelectedDateRight")

    send_mail = 0

    for i in range(day_range):
    
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

            send_mail = 1
            
        
        # GO TO NEXT DAY
        next_day.click()
        time.sleep(2)


    if get_send_status() == 1 and send_mail == 1:
        # CALL integromat REQUEST SENDER FUNCTION
        send_mail_request("nika.kobaidze@gmail.com", "Mail text")
        
        # DISABLE REQUEST SENDING
        set_send_status(0)
        print('[INFO] - Mail Sent')
        
    else:
        print('[INFO] - Mail Not Send...')

    
    # THIS MEANS THAT THERE IS NO DAY FOUND IN DATE RANGE
    # ENABLE MAIL SENDING
    if send_mail == 0:
        set_send_status(1)


# job()
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)