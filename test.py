import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import re

PRICE_REGEX = re.compile(r"^(\d+)")

def get_name(driver):
    try:
        name_element = driver.find_element(By.CSS_SELECTOR, "h1.AdDecriptionVeh_adTitle__vEuKD[itemprop='name']")
        return name_element.text
    except Exception as e:
        print(f"Error getting name: {e}")
        return None

def get_price(driver):
    try:
        price_detail = driver.find_element(By.CSS_SELECTOR, "span[itemprop='price']")
        price_real = PRICE_REGEX.findall(price_detail.text.replace(".", ""))
        return int(price_real[0]) if price_real else None
    except Exception as e:
        print(f"Error getting price: {e}")
        return None

def get_location(driver):
    try:
        position_element = driver.find_element(By.CSS_SELECTOR, "span.fz13")
        return position_element.text
    except Exception as e:
        print(f"Error getting location: {e}")
        return None

def scrape_data(driver):
    try:
        wait = WebDriverWait(driver, 5)
        button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "styles_button__SVZnw")))
        button.click()

        brand = None
        brand_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Hãng:')]/following-sibling::span/a")
        if brand_element:
            brand = brand_element.text

        model = None
        model_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Dòng xe:')]/following-sibling::a")
        if model_element:
            model = model_element.text
        
        # Similarly, fetch other details
        
        return brand, model  # Return other details as well
    except Exception as e:
        print(f"Error scraping data: {e}")
        return None, None  # Handle other details similarly

def crawl_data(url):
    webdriver_path = "D:\HK6\Tool\msedgedriver.exe"
    service = Service(webdriver_path)
    options = Options()
    driver = webdriver.Edge(service=service, options=options)

    with driver:
        try:
            driver.get(url)
            price = get_price(driver)
            name = get_name(driver)
            location = get_location(driver)
            brand, model = scrape_data(driver)
            return name, price, location, brand, model
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            return None, None, None, None, None

def main(urls):
    data = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(crawl_data, url) for url in urls]

        for future in as_completed(futures):
            try:
                name, price, location, brand, model = future.result()
                if name:
                    data.append({'name': name, 'price': price, 'location': location, 'brand': brand, 'model': model})
            except Exception as e:
                print(f"Error processing future result: {e}")

    return data

if __name__ == "__main__":
    df = pd.read_csv('url.csv')
    urls = df['URL'].tolist()

    start_time = time.time()
    final_data = main(urls)
    end_time = time.time()
    print("Crawl time: ", end_time - start_time, "s")

    df = pd.DataFrame(final_data)
    df.to_csv('datat_test.csv', index=False)
