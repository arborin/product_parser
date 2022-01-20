from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as SelenimumTimeout

import requests
import time



class HeadlessChrome():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('user-data-dir=C:\\Users\\charles.fawole\\AppData\\Local\\Google\\Chrome\\User Data\\Default') #use my browser cookies to log into webpage
        #chrome_options.add_argument("headless"); 
        driver_path = r"C:\Users\User\Desktop\chromedriver.exe"
        self.driver = webdriver.Chrome(driver_path, options=chrome_options)  # Optional argument, if not specified will search path.
        
        
        #self.driver.set_window_position(-10000,0) #minimize browser. double check to see it this acutually works


    def close_browser(self):
        self.driver.quit()

    def get_page_source(self):
         page_source = (self.driver.page_source)
         return page_source

    def get_page(self, url):
         return self.driver.get(url)

    def close_browser(self):
        self.driver.quit()

    def scroll_page(self,n_times = 1,sleep_time=0):
        for i in range(n_times):
            time.sleep(sleep_time)
            print("scrolling...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scoll probaly causes overlap in scraped record. Not scolling enough, it seems

    def create_element_by_xpath(self,xpath,timeout):
        web_element  = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath)))

        return web_element
        
    
