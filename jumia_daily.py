import os
import pandas as pd
from datetime import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import threading



products = pd.read_csv("tracking.csv")
day_date = datetime.now().strftime("%d-%m-%Y")
day_file_name = "prices_{}.csv".format(day_date)
isFile = os.path.isfile(day_file_name)

if not isFile:
    day_products_csv = pd.DataFrame(columns=["product_id", "product_name", "product_link", "product_price", "product_old_price", "product_discount", "Date"])
    day_products_csv["product_id"] = products["product_id"]
    day_products_csv["product_name"] = products["product_name"]
    day_products_csv["product_link"] = products["product_link"]
    day_products_csv.to_csv(day_file_name, index=False)

day_prices = pd.read_csv(day_file_name)

grouped_links = [day_prices.product_link[i:i+5] for i in range(0, len(day_prices.product_link)-4, 5)]


folder_name = "products_{}".format(day_date)
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

def download_page(product_link, folder_name):
  
    try:
        product_file_name = product_link.split('/')[-1]
        isFile = os.path.isfile("{}/{}".format(folder_name, product_file_name))
       
        if not isFile:
            req = Request(
                url=product_link, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )

            webpage = urlopen(req).read()
            
            with open("{}/{}".format(folder_name, product_file_name), "wb") as f:
                f.write(webpage)
        else:
            print("File exist")
    
    except:
        print("Unable to Download: {}".format(product_link))


for links in grouped_links[::-1]:
    threads = []

    for product_link in links:
        print("Downloading: {}".format(product_link))
        thread = threading.Thread(target=download_page, args=[product_link, folder_name])
        thread.start()
        threads.append(thread)
        print(f'Active Threads: {threading.active_count()}')
        
    for thread in threads:
        thread.join()
    
    

print("Tracked")

