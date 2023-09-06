import random
import time
from sizes import SIZE_TABLE
from selenium.webdriver.support.wait import WebDriverWait
from agents import USER_AGENTS_LIST
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC

sku = input("input SKU: ")

url = f"https://stockx.com/search?s={sku}"

service = Service(ChromeDriverManager().install())

person = random.choice(USER_AGENTS_LIST)
persona = {
    'user-agent': person
}
options = ChromeOptions()
options.add_argument(f"user-agent={persona['user-agent']}")
options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options, service=service)
wait = WebDriverWait(driver, 40)

driver.get(url)

first_found = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#browse-grid'))).find_element(By.TAG_NAME,
                                                                                                         'a')
href = first_found.get_attribute('href')
new_href = href.replace("https://stockx.com/", "https://stockx.com/buy/")

driver.get(new_href)
time.sleep(1)
coockie = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-button-group > div.accept-btn-container")))
time.sleep(1)
coockie.click()

time.sleep(3)
try:
    but_us = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.css-qip28k:nth-child(1)')))
    time.sleep(3)
    driver.execute_script("arguments[0].click();", but_us)
except:
    pass
price_ = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-4tso23"))).text
price_size = []
lines = price_.split("\n")
for i in range(0, len(lines), 2):
    size = lines[i]
    price = lines[i + 1]
    price_size.append([size, price])
print(price_size)

url = 'https://restocks.net/nl/login'
login = "luca.drago23@gmail.com"
password = "YJkbM5XYSh2jyEi"

driver.get(url)
login_in = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#email')))
login_in.send_keys(login)

pass_in = driver.find_element(By.CSS_SELECTOR, '#password')
pass_in.send_keys(password)

lang_button = driver.find_element(By.CSS_SELECTOR,
                                  '.modaal-content-container > div:nth-child(1) > button:nth-child(1) > div:nth-child(1)')
lang_button.click()
try:
    butt_coockie = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.cc-btn')))
    time.sleep(0.5)
    butt_coockie.click()
except:
    pass
button_auth = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#submit__button')))
time.sleep(1)
button_auth.click()
# #topbar__right__default > a:nth-child(1)
but_shell = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#topbar__right__default > a:nth-child(1)')))
but_shell.click()

butt_acept = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.margin-top-1-5em')))
butt_acept.click()
# #baseproduct_id
your_sku = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#baseproduct_id')))
your_sku.send_keys(sku)
# .product-item__image
click_prod = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.product-item__image')))
time.sleep(1)
click_prod.click()
##condition
origin_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#condition')))
time.sleep(1)
origin_box.click()
# condition > option:nth-child(2)
confim = origin_box.find_element(By.CSS_SELECTOR, '#condition > option:nth-child(2)')
confim.click()

selest_size = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#size_id')))
selest_size.click()
lines = selest_size.text

result = []
for line in lines.split('\n'):
    size = line.strip().replace('½', '.5').replace(' ', '').replace('\t', '')
    size = size.replace(' .5', '.5').replace('.5 ', '.5').replace(',', '.')
    if size:
        result.append(size)

new_us_price = []
for row in price_size:
    size = row[0].split()[2]
    euro_size = SIZE_TABLE['us'].get(size)
    if euro_size:
        euro_price = row[1]
        if euro_price != 'Bid' and 'bid':
            euro_price = euro_price.replace(',', '.')
            euro_price = float(euro_price[1:])
            euro_price = round((euro_price + (euro_price * 0.1)) + 20, 2)
            euro_price = str(euro_price)
        new_row = [row[0].replace(size, euro_size), euro_price]
        new_us_price.append(new_row)
print(new_us_price)

count = 0
for row in new_us_price:
    size = row[0].split()[2]
    euro_index = result.index(size)
    price = row[1]
    print(price)
    size = selest_size.find_element(By.CSS_SELECTOR, f'#size_id > option:nth-child({euro_index + 1})')
    time.sleep(1.5)
    size.click()
    your_price = driver.find_element(By.CSS_SELECTOR, '#store_price')
    time.sleep(1)
    your_price.send_keys(round(price))
    sell_metod = driver.find_element(By.CSS_SELECTOR, '#sell_method')
    time.sleep(1)
    sell_metod.click()
    metod = sell_metod.find_element(By.CSS_SELECTOR, '#sell_method > option:nth-child(2)')
    time.sleep(1)
    metod.click()
    day = driver.find_element(By.CSS_SELECTOR, '#duration')
    time.sleep(1)
    day.click()
    count_day = day.find_element(By.CSS_SELECTOR, '#duration > option:nth-child(3)')
    count_day.click()
    i_agree = driver.find_element(By.CSS_SELECTOR,
                                  'div.checkbox__block:nth-child(9) > label:nth-child(1) > span:nth-child(3)')
    i_agree.click()
    i_hereby = driver.find_element(By.CSS_SELECTOR,
                                   'div.checkbox__block:nth-child(9) > label:nth-child(2) > span:nth-child(2)')
    i_hereby.click()
    next_step = driver.find_element(By.CSS_SELECTOR, '#next__button')
    time.sleep(2)
    next_step.click()
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#submit__button')))
    time.sleep(2)
    button.click()
    but_shell = (EC.element_to_be_clickable((By.CSS_SELECTOR, '#topbar__right__default > a.sell__button')))
    time.sleep(2)
    but_shell.click()
    butt_acept = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.margin-top-1-5em')))
    time.sleep(2)
    butt_acept.click()
    your_sku = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#baseproduct_id')))
    your_sku.send_keys(sku)
    click_prod = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.product-item__image')))
    time.sleep(1)
    click_prod.click()
    origin_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#condition')))
    time.sleep(1)
    origin_box.click()
    confim = origin_box.find_element(By.CSS_SELECTOR, '#condition > option:nth-child(2)')
    confim.click()
    selest_size = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#size_id')))
    selest_size.click()
    time.sleep(2)

driver.quit()
