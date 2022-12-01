from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep  
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from pytz import timezone
import pandas as pd
import os.path
from os import path
from urllib.parse import urlparse, parse_qs
import urllib.request
# import gspread
# from gspread.exceptions import SpreadsheetNotFound
# from oauth2client.service_account import ServiceAccountCredentials
# from datetime import date
# from gspread_dataframe import get_as_dataframe, set_with_dataframe


website_url = 'https://www.jumia.com.ng/'
cat_url = 'https://www.jumia.com.ng/computing/'


def main():

    print("Initializing....")
    
    # start a new brower 
    print("Start the browser")
    browser = start()

    # visit a page in the browser
    print("Visiting {}".format(website_url))
    browser.get(website_url)
    
    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cat > a.tit")))
    
    # select all url for main categories
    categories = browser.find_elements(By.CSS_SELECTOR, ".cat > a.tit ")
    category_links = []

    for category in categories:
        link = category.get_attribute('href')
        if link is not None:
            category_links.append(link)


    category_links = list(set(category_links))

    for category_link in category_links:
        
      
        
        get_page_products(browser, category_link)

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.pg")))
        url = browser.find_element(By.CSS_SELECTOR, "a.pg:last-child").get_attribute('href')
        
        parse_result = urlparse(url)
        dict_result = parse_qs(parse_result.query)
        print(url)
        print(int(dict_result['page']))

        print(de)
        print(D)
        # last_page = int(dict_result['page'][0])
        for i in range(50):
            page_link = category_link + "?page={}#catalog-listing".format(i+2)
            get_page_products(browser, page_link)
            break
        break   
    print(d)
    print("done")

    

def get_page_products(browser, page_link):
    
    wait = WebDriverWait(browser, 10)
    browser.get(page_link)
    total_height = browser.find_element(By.CSS_SELECTOR, "body").size['height']
    print(total_height)
    for h in range(0, total_height, 15):
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
            print(page_product.find_element(By.CSS_SELECTOR, "a.core").get_attribute('href'))
        except NoSuchElementException:
            print("Missing link")
        try:
            print(page_product.find_element(By.CSS_SELECTOR, "h3.name").text)
        except NoSuchElementException:
            print("Missing name")

        try:
            print(page_product.find_element(By.CSS_SELECTOR, "div.prc").text)
        except NoSuchElementException:
            print("Missing Price")

        try:
            print(page_product.find_element(By.CSS_SELECTOR, ".s-prc-w > .old").text)
        except NoSuchElementException:
            print("Missing Old price")
        try:
            print(page_product.find_element(By.CSS_SELECTOR, ".s-prc-w .bdg._dsct._sm").text)
        except NoSuchElementException:
            print("Missing Old Discount")
    

def start():
    directory = os.getcwd()
    path_to_chromedriver = directory + '\\browser\chromedriver106.exe' # change path as needed
    browser = webdriver.Chrome(executable_path = path_to_chromedriver) #use chrome driver as browser
    # browser = webdriver.Chrome() #use chrome driver as browser mac
    browser.maximize_window() #maximize window
    
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = (
    #      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    #      "(KHTML, like Gecko) Chrome/15.0.87")

    # path_to_phantomjs = 'C:\Program Files (x86)\chromedriver\bin\phantomjs.exe' # change path as needed
    # browser = webdriver.PhantomJS(executable_path = path_to_phantomjs)
    # browser = webdriver.PhantomJS(executable_path = path_to_phantomjs, desired_capabilities = dcap)
    return browser



# close date in format %d_%m_%Y '26_05_2020'
def open_spreadsheet(gs_client, name="Mobile Carrier Liquidation"):
    try:
        spreadsheet = gs_client.open(name)
        print("Found old spreadsheet, opening")
    except SpreadsheetNotFound:
        print("Not found, creating")
        spreadsheet = gs_client.create(name)
    
    spreadsheet.share('alabamustapha@gmail.com', perm_type='user', role='writer', notify=False)
    spreadsheet.share('federico@cirkuitplanet.com', perm_type='user', role='writer', notify=False)

    return spreadsheet
    
# start the google client that help to connect to spreadsheets
def start_gs_client():

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('mobile-carrier-data-f137413b4305.json', scope)
    gs_client = gspread.authorize(credentials)

    return gs_client



if __name__ == "__main__": main()


