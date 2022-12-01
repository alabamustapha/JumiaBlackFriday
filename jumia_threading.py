import threading
import time
import concurrent.futures

def scrape_category(category_name, category_link):
    print(f'Scrapping {category_name} from {category_link}', end = "\n")
    time.sleep(3)
    print(f'Done Scrapping {category_name} from {category_link}', end = "\n")


categories = [
    ['category-fashion-by-jumia', 'https://www.jumia.com.ng/category-fashion-by-jumia/'],
    ['electronics', 'https://www.jumia.com.ng/electronics/'],
    ['phones-tablets','https://www.jumia.com.ng/phones-tablets/'],
    ['computing', 'https://www.jumia.com.ng/computing/']
]


threads = []
start = time.perf_counter()

# for category in categories:
#     thread = threading.Thread(target=scrape_category, args=category)
#     thread.start()
#     threads.append(thread)
#     print(f'Active Threads: {threading.active_count()}')
    

# for thread in threads:
#     thread.join()

with concurrent.futures.ThreadPoolExecutor() as executor:
     executor.map(scrape_category, categories)

end = time.perf_counter()
print(f'Finished in {round(end-start, 2)} second(s)') 