import os
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd



def get_product_details(file_path, file_name):
    file_path = "{}\{}".format(path, file_name)
    product_detail = [file_name]
    
    timestamp = os.path.getctime(file_path)

    file_datetime = datetime.fromtimestamp(timestamp)
    product_detail.append(file_datetime)

    with open(file_path, 'r', encoding='utf-8') as f:
        product_page_content = f.read()

        product_page_soup = BeautifulSoup(product_page_content, 'html.parser')

        has_bf_label = 1 if product_page_soup.find("img", attrs={"alt": "BF22"}) is not None else 0
        product_detail.append(has_bf_label)

        product_name = product_page_soup.find('h1').get_text()
        product_detail.append(product_name)

        product_categories = [cat.get_text() for cat in product_page_soup.select('.brcbs a.cbs')[1:-1]]
        product_detail.append(",".join(product_categories))

        product_price_info_div = product_page_soup.find('div', class_="-hr -mtxs -pvs")


        if product_price_info_div.find('span', class_="-b -ltr -tal -fs24"):
            product_price = product_price_info_div.find('span', class_="-b -ltr -tal -fs24").get_text()
        else:
            product_price = None

        product_detail.append(product_price)

        if product_price_info_div.find('span', class_="-tal -gy5 -lthr -fs16"):
            product_old_price = product_price_info_div.find('span', class_="-tal -gy5 -lthr -fs16").get_text()
        else:
            product_old_price = None

        product_detail.append(product_old_price)

        if product_price_info_div.find('span', class_="bdg _dsct _dyn -mls"):
            product_percentage = product_price_info_div.find('span', class_="bdg _dsct _dyn -mls").get_text()
        else:
            product_percentage = None

        product_detail.append(product_percentage)

        return product_detail



# iterate through all file
error_count = 0
for day in range(27, 29):
    products_details_list = []
    day_filename = "products_{:02d}-11-2022".format(day)
    path = os.getcwd() + "\products_{:02d}-11-2022".format(day)
    print("Running for path: {}".format(path))
    
    for file_name in os.listdir(path):
        try:
            product_details = get_product_details(path, file_name)
            products_details_list.append(product_details)
        except Exception as e:
            error_count = error_count + 1
            # print("-" * 100)
            # print("Error in {}".format("{}\{}".format(path, file)))
            # print(e)
        
    df = pd.DataFrame(products_details_list, columns=['file_name', 'file_datetime', 'has_bf_label', 'product_name', 'product_categories', 'product_price', 'product_old_price', 'product_percentage'])
    df.to_csv('{}_combined.csv'.format(day_filename))
    

print(error_count)