import requests
from bs4 import BeautifulSoup
import csv
import sys

# CHANGE THIS URL IF YOU WANT
base_url = "https://www.breuninger.com/de/herren/bekleidung/"

# PRODUCT LIMIT FOR CRPDUCT
# SET -1 FOR GET ALL RECORDS
product_limit = 10

# 
page = requests.get(base_url)
soup = BeautifulSoup(page.content, 'html.parser')

# GET HOW MANY PAGES ARE IN THIS CATEGORY
last_page = soup.find_all('span', class_="suchen-pager__size")
last_page = int(last_page[0].text)


# INFO
print("------------------------------------------------")
print("Getting Data from: {}".format(base_url))
print("Total pages: {}".format(last_page))
print("------------------------------------------------")
print("Brand, Description, Color")  
print("================================================")


# CREATE CSV FILE SAME DIRECTORY
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Brand", "Description", "Color"])

    total_products = 0 # counter for info

    # LOOP PAGES FROM 1 TO last_page
    for curent_page in range(1, last_page+1):

        if total_products == product_limit:
            break;

        url = "{}?page={}".format(base_url, curent_page)

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # GET PRODUCT LIST FORM THIS PAGE
        products = soup.find_all('div', class_='suchen-produktliste__item suchen-produktliste__item--produkt')

        # COLLECT ALL PRODUCT LINKS
        product_details_link = []

        for pr in products:
            product_details_link.append(pr.find_all('a')[0]['href'])
        

        # OPEN EVERY LINK ON THIS PAGE
        for link in product_details_link:

            if total_products == product_limit:
                break;

            url = "https://www.breuninger.com{}".format(link)
            details = requests.get(url)
            details_soap = BeautifulSoup(details.content, 'html.parser')
            
            # BRAND
            brand = details_soap.find_all("span", {"itemprop": "name"})[0].text.strip()
            
            # DESCRIPTION
            desc = details_soap.find_all("span", class_="bewerten-zusammenfassung__name")[0].text.strip()

            # COLOR
            # example "Farbe: SCHWARZ"
            color = details_soap.find_all('div', class_="bewerten-farben__aktiv")[0].text.strip()
            # ['Farbe', ' SCHWARZ']
            color = color.split(":")[1].strip()
            
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