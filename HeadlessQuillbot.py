from typing import Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as SelenimumTimeout
from selenium.common.exceptions import ElementNotInteractableException
from HeadlessChrome import HeadlessChrome

import time

class HeadlessQuillbot(HeadlessChrome):
    def __init__(self):
        super().__init__()

    def summarize_text(self,full_text, time_before_summarize_click=10, time_allowance_for_processing=20):
        # in_textbox = "/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div/div/div/div[2]/div[1]/div/div[1]/div"
        in_textbox = WebDriverWait(self.driver, 20).until(EC.visibility_of_all_elements_located((By.ID, "inputBoxSummarizer")))

        # in_textbox  = WebDriverWait(self.driver, 50).until(
        #     EC.presence_of_all_elements_located((By.XPATH, in_textbox)))

        in_textbox[0].send_keys(full_text)
        

        # summarize_btn = "/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div/div/div/div[2]/div[3]/div[1]/div/div/div/div[2]/div/div/div/button"
        # summarize_btn  = WebDriverWait(self.driver, 50).until(
        #     EC.presence_of_all_elements_located((By.XPATH, summarize_btn)))

        summarize_btn = WebDriverWait(self.driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "false")))
        
        
        time.sleep(time_before_summarize_click) #leave enough time to let text be input before clicking summarize
        summarize_btn[0].click()

        time.sleep(time_allowance_for_processing) #wait and let the bot do its thing
        # output_summary_textbox = "/html/body/div[1]/div[2]/div[3]/div/div/div[1]/div/div/div/div[2]/div[2]/div/div"

        # output_summary_textbox = WebDriverWait(self.driver, 10).until(
        #             EC.presence_of_all_elements_located((By.XPATH, output_summary_textbox)))

        output_summary_textbox = WebDriverWait(self.driver, 20).until(EC.visibility_of_all_elements_located((By.ID, "outputBoxSummarizer")))
        summary = output_summary_textbox[0].text
        
        return summary

def main():

    headless = HeadlessQuillbot()

    headless.get_page('https://quillbot.com/summarize')
    summary = headless.summarize_text("Hello. How are you?")
    print(summary)
    
main()
