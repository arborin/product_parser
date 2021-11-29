# SETUP
# 1. INSTALL selenium  
# pip install -U selenium

# 2. INSTALL BeautifulSoup 
# pip install bs4

# 3. INSTALL lxml library 
# pip install lxml

# 4. DOWNLOAD CHROME DRIVER: 
# https://chromedriver.storage.googleapis.com/index.html?path=96.0.4664.45/
# browser = webdriver.Chrome(r"FULL_PATH_OF_WEBDRIVER.EXE !!!")



import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv


# SETTINGS
url = "https://en.zalando.de/mens-clothing/"
driver_path = r"C:\Users\admin\Desktop\chromedriver.exe"

product_limit = 100  # SET -1 TO GET ALL PRODUCTS
total_products = 0  # PRODUCT COUNTER, DON'T CHANGE
# END SETTINGS


chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--log-level=3')



# METHOD 1
# SNED GET REQUEST ! not loading page full
# SET HEADERS FOR SENDING REQUEST AS BROWSER
# OTHERWISE IT NOT RESPONDING
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# response = requests.get(url, headers=headers)


# METHOD 2 
# USE urllib 
# response = urllib.request.urlopen(url)
# html = response.read().decode('utf-8')

# METHOD 3
# WORKING METHOD REQUIRE ADDITIONAL INSTALL selenium AND DOWNLOAD chromedriver
# pip install -U selenium
# https://chromedriver.chromium.org/home



# FIND ALL PAGES COUNT
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(url, headers=headers).content
soup = BeautifulSoup(response, 'lxml')

# GET PAGES
page_text = soup.find_all("span", attrs={'aria-current': True})[0].text
# CONTENT EXAMPLE: Page 1 of 428
last_page = page_text.split(" ")[-1] # GET LAST ELEMENT 428
print("=========================================================")
print(f"URL: {url}")
print(f"TOTAL PAGES: {last_page}")
# END ALL PAGES COUNT


# CREATE CSV FILE SAME DIRECTORY
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Brand", "Description", "Color"])

    # LOOP FOR ALL PAGES
    for page in range(1, 3):

        # CHECK PRODUCT LIMIT
        if total_products == product_limit:
            break;

        # GENERATE URL
        page_url = "{}?p={}".format(url, page)

        # INFO
        print("=========================================================")
        print(page_url)
        
        browser = webdriver.Chrome(driver_path, options=chrome_options)
        browser.set_script_timeout(5)
        browser.get(page_url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        # GETING ALL "article" TAGS 
        articles = soup.find_all('article')

        # INFO
        print(f"product on page: {len(articles)}")
        print("=========================================================")

        page_links = []

        for i, article in enumerate(articles):
            if "https" in article.a['href']:
                page_links.append(article.a['href'])
                # print("{} -- {}".format(i, article.a['href']))


        # OPEN PAGE LINKS AND GET DATA FROM IT
        for page_link in page_links:

            # CHECK PRODUCT LIMIT
            if total_products == product_limit:
                break;
            
            print(page_link)
            page_html = requests.get(page_link, headers=headers).content
            page_soup = BeautifulSoup(page_html, 'lxml')

            wrapper = page_soup.find("x-wrapper-re-1-4")
            
            try:
                brand = wrapper.a.text
            except:
                brand = "BRAND NOT FOUND"

            try:
                desc = wrapper.h1.text
            except:
                desc = "DESC NOT FOUND"

            try:
                search_color = wrapper.find_all("span")
                color_span = ""
                for span_num, span in enumerate(search_color):
                    if span.text=="Colour:":
                        color_span = span_num + 1 # next span is color
                        break;
                    
                    # print(span.text)
                if color_span != "":
                    color = search_color[color_span].text
                else:
                    color = "COLOR NOT FOUND"

            except:
                color = "COLOR NOT FOUND"
        
            
            # INFO
            print("{},{},{}".format(brand, desc, color))
            
            # WRITE INTO CSV FILE
            writer.writerow([brand, desc, color])
            total_products += 1


file.close()
# INFO
print("------------------------------------------------")
print("Total products add: {}".format(total_products))
print("End")  
print("------------------------------------------------")
        
