import os
import pandas as pd

def get_files_in_csv_dir(csv_path='csv'):
    file_names = []
    for root, directories, files in os.walk(csv_path):
        for name in files:
            if(name[-4:] == '.csv'):
                file_names.append(os.path.join(root, name))

    return file_names


file_names_02 = get_files_in_csv_dir("02-11-2022")
file_names_03 = get_files_in_csv_dir("03-11-2022")

file_names = file_names_02 + file_names_03

products_df = pd.DataFrame(columns =["product_id", "product_name", "product_link", "product_price", "product_old_price", "product_discount", "Date"])


for file_name in file_names:
    products = pd.read_csv(file_name)
    products_df = pd.concat([products_df, products], keys=["product_id", "product_name", "product_link", "product_price", "product_old_price", "product_discount", "Date"], ignore_index = True)
    

products_df.drop_duplicates(subset="product_id", inplace=True)
products_df.to_csv("tracking.csv")

print("Tracked")