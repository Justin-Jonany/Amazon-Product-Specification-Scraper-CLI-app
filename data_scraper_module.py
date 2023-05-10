from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time

def get_items(driver):
    time.sleep(3) # FIX THIS, change
    items = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
    return items


def get_names(items, list_name):
    for item in items:
        name = item.find_element(By.XPATH, ".//span[contains(@class, 'a-color-base a-text-normal')]")
        list_name.append(name.text)

def get_asin(items, list_asin):
    for item in items:
        asin = item.get_attribute("data-asin")
        list_asin.append(asin)

def get_price(items, list_price):
    for item in items:
        whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
        fraction_price = item.find_elements(By.XPATH,'.//span[@class="a-price-fraction"]')
        if whole_price != [] and fraction_price != []:
               price = '.'.join([whole_price[0].text, fraction_price[0].text])
        else:
            price = 0

        list_price.append(price)

def get_rating(items, list_rating, list_rating_num):
    for item in items:
        ratings_box = item.find_elements(By.XPATH, ".//div[@class='a-row a-size-small']/span")
        if len(ratings_box) == 2:
            ratings = ratings_box[0].find_element(By.CLASS_NAME, "a-size-base")
            ratings_num = ratings_box[1].get_attribute("aria-label")
            list_rating.append(ratings.text)
            list_rating_num.append(str(ratings_num))
        else:
            ratings, ratings_num = 0, 0
            list_rating.append(ratings)
            list_rating_num.append(ratings_num)

        
