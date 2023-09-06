import os
import random
import time
from sizes import SIZE_TABLE
from selenium.webdriver.support.wait import WebDriverWait
from agents import USER_AGENTS_LIST
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import Firefox


class Parser:
    def __init__(self, sku):
        self.sku = sku
        self.url = f"https://stockx.com/search?s={sku}"
        self.service = Service(GeckoDriverManager().install())
        self.person = random.choice(USER_AGENTS_LIST)
        self.next_url = 'https://restocks.net/nl/login'
        self.log, self.passworld = self.get_login_pas()
        self.count = 0

    def get_login_pas(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(current_dir, 'login_passworld.txt')
        with open(filename) as f:
            data = f.read().strip().split(':')
            username = data[0]
            password = data[1]
        return username, password

    def init_driver(self):
        options = Options()
        options.add_argument(f"user-agent={self.person}")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.page_load_strategy = 'normal'
        # options.add_argument("--headless=new")
        return options

    def pars_shoe(self, options):
        driver = Firefox(options=options, service=self.service)
        driver.get(self.url)
        time.sleep(random.randint(2, 7))
        wait = WebDriverWait(driver, 40)
        coockie = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-button-group > div.accept-btn-container")))
        time.sleep(1)
        coockie.click()
        first_found = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#browse-grid'))).find_element(
            By.TAG_NAME,
            'a')
        time.sleep(random.randint(1, 3))
        href = first_found.get_attribute('href')
        driver.get(href)
        time.sleep(random.randint(10, 20))
        prices = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.css-xopws2 > p:nth-child(1)')))
        time.sleep(random.randint(1, 3))
        prices.click()
        # href = first_found.get_attribute('href')
        # new_href = href.replace("https://stockx.com/", "https://stockx.com/buy/")
        # driver.get(new_href)
        # time.sleep(random.randint(10, 20))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
        time.sleep(random.randint(15, 20))
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        time.sleep(1)
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
        return driver, wait, price_size

    def enter_site(self, driver, wait):
        driver.get(self.next_url)
        login_in = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#email')))
        login_in.send_keys(self.log)

        pass_in = driver.find_element(By.CSS_SELECTOR, '#password')
        pass_in.send_keys(self.passworld)
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
        try:
            button_auth.click()
        except:
            driver.execute_script("arguments[0].click();", button_auth)

    def preparation(self, wait):
        time.sleep(random.randint(1, 5))
        self.count += 1
        but_shell = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#topbar__right__default > a:nth-child(1)')))
        but_shell.click()
        butt_acept = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.margin-top-1-5em')))
        butt_acept.click()
        your_sku = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#baseproduct_id')))
        your_sku.send_keys(self.sku)
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
        lines = selest_size.text
        return lines, selest_size

    def results_processing(self, lines, price_size):
        result = []
        for line in lines.split('\n'):
            size = line.strip().replace('½', '.5').replace(' ', '').replace('\t', '')
            size = size.replace(' .5', '.5').replace('.5 ', '.5').replace(',', '.')
            if size:
                result.append(size)
        new_us_price = []
        for row in price_size:
            if len(row[0].split()) >= 3:
                size = row[0].split()[2]
                euro_size = SIZE_TABLE['us'].get(size)
                if euro_size:
                    euro_price = row[1]
                    if euro_price != 'Bid':
                        euro_price = euro_price.replace(',', '.')
                        euro_price = float(euro_price[1:])
                        euro_price = round((euro_price + (euro_price * 0.1)) + 20)
                        euro_price = str(euro_price)
                    new_row = [row[0].replace(size, euro_size), euro_price]
                    new_us_price.append(new_row)
        new_us_price = [x for x in new_us_price if x[1] != '']
        return result, new_us_price

    def add_to_site(self, result, new_us_price, driver, wait, selest_size):
        print(new_us_price)
        count = 0
        for row in new_us_price:
            if count >= 1:
                if count % 5 == 0:
                    time.sleep(random.randint(10, 20))
                selest_size = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#size_id')))
                time.sleep(0.5)
                selest_size.click()
            size = row[0].split()[2]
            try:
                euro_index = result.index(size)
            except:
                count += 1
                self.preparation(wait)
                continue
            price = row[1]
            try:
                time.sleep(random.randint(2, 7))
                size = selest_size.find_element(By.CSS_SELECTOR, f'#size_id > option:nth-child({euro_index + 2})')
            except Exception as e:
                count += 1
                self.preparation(wait)
                continue
            time.sleep(random.randint(2, 5))
            size.click()
            print(price)
            if price == 'Bid':
                count += 1
                self.preparation(wait)
                continue
            your_price = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#store_price')))
            time.sleep(1)
            your_price.send_keys(price)
            sell_metod = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#sell_method')))
            time.sleep(1)
            sell_metod.click()
            metod = sell_metod.find_element(By.CSS_SELECTOR, '#sell_method > option:nth-child(2)')
            time.sleep(1)
            metod.click()
            day = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#duration')))
            time.sleep(1)
            day.click()
            count_day = day.find_element(By.CSS_SELECTOR, '#duration > option:nth-child(3)')
            count_day.click()
            i_agree = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                 'div.checkbox__block:nth-child(9) > label:nth-child(1) > span:nth-child(3)')))
            i_agree.click()
            i_hereby = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                  'div.checkbox__block:nth-child(9) > label:nth-child(2) > span:nth-child(2)')))
            i_hereby.click()
            next_step = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#next__button')))
            time.sleep(random.randint(2, 5))
            next_step.click()
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#submit__button')))
            time.sleep(random.randint(2, 6))
            button.click()
            time.sleep(random.randint(2, 7))
            print(f'Product added!')
            count += 1
            self.preparation(wait)
        print(f'all products added successfully!')

    def run(self):
        options = self.init_driver()
        driver, wait, price_size = self.pars_shoe(options)
        self.enter_site(driver, wait)
        lines, selest_size = self.preparation(wait)
        result, new_us_price = self.results_processing(lines, price_size)
        self.add_to_site(result, new_us_price, driver, wait, selest_size)


sku = input("input SKU: ")
check = Parser(sku=sku)
check.run()
# Nike Dunk Low Retro While Black Panda