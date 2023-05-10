from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import data_scraper_module
import sys

url = "https://www.amazon.com/"
PATH = "/usr/local/bin/chromedriver"
product_name = []
product_asin = []
product_price = []
product_ratings = []
product_ratings_num = []
product_link = []

def search(item, driver):
    search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
    search.send_keys(item)
    search.send_keys(Keys.RETURN)
    driver.implicitly_wait(5)
# products = [driver.find_element(By.XPATH, productPath.format(productNum = i)) for i in range(2, 5, 1)]

def get_data(driver, items):
    data_scraper_module.get_names(items=items, list_name=product_name)
    data_scraper_module.get_asin(items=items, list_asin=product_asin)
    data_scraper_module.get_price(items=items, list_price=product_price)
    data_scraper_module.get_rating(items=items, list_rating=product_ratings, list_rating_num=product_ratings_num)

def print_data():
    print("Item names: ", product_name)
    print("Item asin: ", product_asin)
    print("Item price: ", product_price)
    print("Item rating: ", product_ratings)
    print("Item rating number: ", product_ratings_num)


def change_page(driver, page):
    current_page = int(driver.find_element(By.XPATH, ".//span[@class='s-pagination-item s-pagination-selected']").text)
    page_difference = abs(page - current_page)
    if (page > current_page):
        for i in range(page_difference):
            next_button = driver.find_element(By.XPATH, ".//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
            next_button.click()
    else:
        for i in range(page_difference):
            back_button = driver.find_element(By.XPATH, ".//a[@class='s-pagination-item s-pagination-previous s-pagination-button s-pagination-separator']")
            back_button.click()




def main():
    chrome_options = Options()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options, service=Service(PATH))
    driver.get(url)
    
    if len(sys.argv) <= 1:
        print("Usage: Python3 amazon_scraper.py <item> [page]", file=sys.stderr)
        quit()
    elif len(sys.argv) == 2:
        item = sys.argv[1]
        page = 1
    else:
        item = sys.argv[1]
        page = int(sys.argv[2])
        
    search(item=item, driver=driver)
    pages_available = int(driver.find_element(By.XPATH, ".//span[@class='s-pagination-item s-pagination-disabled']").text)
    if pages_available < page:
        message = "Page out of bounds; Number of pages for item '%d' is '%d'"
        print(message.format(item, pages_available))
        quit()
    change_page(driver=driver, page=page)
    items = data_scraper_module.get_items(driver=driver)
    get_data(driver=driver, items=items)
    print_data()
    
    time.sleep(100)
    quit()


if __name__ == "__main__":
    main()