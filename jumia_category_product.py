from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep  
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import os.path
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import pandas as pd
import time
import calendar


# import gspread
# from gspread.exceptions import SpreadsheetNotFound
# from oauth2client.service_account import ServiceAccountCredentials
# from datetime import date
# from gspread_dataframe import get_as_dataframe, set_with_dataframe

# category_name = 'computing'
# cat_url = 'https://www.jumia.com.ng/computing/'

# category_name = 'category-fashion-by-jumia'
# cat_url = 'https://www.jumia.com.ng/category-fashion-by-jumia/'

# category_name = 'electronics'
# cat_url = 'https://www.jumia.com.ng/electronics/'

# category_name = 'phones-tablets'
# cat_url = 'https://www.jumia.com.ng/phones-tablets/'

# category_name = 'groceries'
# cat_url = 'https://www.jumia.com.ng/groceries/'

# category_name = 'home-office'
# cat_url = 'https://www.jumia.com.ng/home-office/'

# category_name = 'selfie-tripods'
# cat_url = 'https://www.jumia.com.ng/selfie-tripods/'





def main():

    products = []

    print("Initializing....")
    
    # start a new brower 
    print("Start the browser")
    browser = start()

    # visit a page in the browser
    print("Visiting {}".format(cat_url))
    browser.get(cat_url)
    
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.pg")))
    url = browser.find_element(By.CSS_SELECTOR, "a.pg:last-child").get_attribute('href')
    parse_result = urlparse(url)
    dict_result = parse_qs(parse_result.query)
    last_page = int(dict_result['page'][0])

    # last_page = int(dict_result['page'][0])
    page_products_list = get_page_products(browser, cat_url)

    save_page_products_to_csv(page_products_list)

    products = products + page_products_list

    
    
    for i in range(2, last_page+1):
        page_link = cat_url + "?page={}#catalog-listing".format(i)
        print(page_link)

        while True:
            try:
                page_products_list = get_page_products(browser, page_link)
                break
            except StaleElementReferenceException:
                print("Stale Exception, page will restart")
                
        save_page_products_to_csv(page_products_list)
        
        products = products + page_products_list


    save_page_products_to_csv(products, 'all')    
    
    print("Done")


def save_page_products_to_csv(page_products_list, filename=None):
    
    products_df = pd.DataFrame(page_products_list, columns =["product_id", "product_name", "product_link", "product_price", "product_old_price", "product_discount", "Date"])
    day_scrapped = datetime.now().strftime("%d-%m-%Y")
    folder_name = '{}/{}'.format(day_scrapped, category_name)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    datetime.now().strftime("%d-%m-%Y")

    if filename is None:
        current_GMT = time.gmtime()
        filename = calendar.timegm(current_GMT)
    products_df.to_csv("{}/{}.csv".format(folder_name, filename))

def get_page_products(browser, page_link):
    
    page_products_list = []

    wait = WebDriverWait(browser, 10)
    browser.get(page_link)
    total_height = browser.find_element(By.CSS_SELECTOR, "body").size['height']
    print(total_height)
    for h in range(0, total_height, 5):
        browser.execute_script("window.scrollTo(0,{})".format(h))
        # break
    page_products_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".prd._fb.col.c-prd")))
    page_products_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.core")))

    page_products = browser.find_elements(By.CSS_SELECTOR, ".prd._fb.col.c-prd")
    print(len(page_products))
    scraped_count = 0
    for page_product in page_products:
        scraped_count = scraped_count  + 1
        print(scraped_count)
        try:
            product_link = page_product.find_element(By.CSS_SELECTOR, "a.core").get_attribute('href')
            product_id = page_product.find_element(By.CSS_SELECTOR, "a.core").get_attribute('data-id')
        except NoSuchElementException:
            product_link = None
            product_id = None
            print("Missing link or ID")
        try:
            product_name = page_product.find_element(By.CSS_SELECTOR, "h3.name").text
        except NoSuchElementException:
            product_name = None
        try:
            product_price = page_product.find_element(By.CSS_SELECTOR, "div.prc").text
        except NoSuchElementException:
            product_price = None
            print("Missing Price")

        try:
            product_old_price = page_product.find_element(By.CSS_SELECTOR, ".s-prc-w > .old").text
        except NoSuchElementException:
            product_old_price = None
            print("Missing Old price")
        try:
            product_discount = page_product.find_element(By.CSS_SELECTOR, ".s-prc-w .bdg._dsct._sm").text
        except NoSuchElementException:
            product_discount = None
            print("Missing Old Discount")
        now = datetime.now()

        product_details = [product_id, product_name, product_link, product_price, product_old_price, product_discount, now]
        page_products_list.append(product_details)

    return page_products_list
def start():
    directory = os.getcwd()
    path_to_chromedriver = directory + '\\browser\chromedriver106.exe' # change path as needed
    browser = webdriver.Chrome(executable_path = path_to_chromedriver) #use chrome driver as browser
    # browser = webdriver.Chrome() #use chrome driver as browser mac
    browser.maximize_window() #maximize window
    
    return browser




if __name__ == "__main__": main()


