import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from concurrent.futures import ThreadPoolExecutor
from tornado import concurrent
import time
from concurrent.futures import ThreadPoolExecutor
from tornado import concurrent
import re

PRICE_REGEX = re.compile(r"^(\d+)")

def get_name(driver):
    # Tìm tất cả các phần tử h1 với class "AdDecriptionVeh_adTitle_vEuKD" và itempprop "name"
    name = None
    try:
        name_element = driver.find_element(By.CSS_SELECTOR, "h1.AdDecriptionVeh_adTitle__vEuKD[itemprop='name']")
        if name_element:
            # Nếu có phần tử, lấy nội dung của phần tử đầu tiên
            name = name_element.text
    except:
        return name
    
    return name

def get_price(driver):
    price_real = None
    try:
        #Tìm phần tử span có itempprop là"price"
        price_detail = driver.find_element(By.CSS_SELECTOR, "span[itemprop = 'price']")
        price_real = price_detail.text
        price_real = PRICE_REGEX.findall(price_real.replace(".", ""))[0]
        price_real = int(price_real)
    except:
        return price_real
    
    return price_real


def get_location(driver):
    #Tìm tất cả phần tử span có class là "fz13"
    position = None
    try:
        position_element = driver.find_element(By.CSS_SELECTOR, "span.fz13")
        if position_element:
            position = position_element.text
    except:
        return position
    
    return position

def get_brand(driver):
    brand_ovil = None
    try:
         brand_get = driver.find_element(By.CSS_SELECTOR, "a.AdParam_asParamValue__IfaYa")
         if brand_get:
              brand_ovil = brand_get.text
    except:
         return brand_ovil
    return brand_ovil
     

def scrape_data(driver):
    brand = None
    model = None
    year_pd = None
    km = None
    status = None
    transmission = None
    fuel = None
    country = None
    style = None
    seat_capacity = None
    payload = None

    try:
        wait = WebDriverWait(driver, 2)
        button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "styles_button__SVZnw")))
        button.click()

        # brand_info_element = driver.find_element(By.CSS_SELECTOR, "div.media-body media-middle")
        # //*[@id="__next"]/div/div[4]/div[1]/div/div[4]/div/div[6]/div[2]/div[1]/div/div[2]/span/a
        
        # brand_info_element = driver.find_elements(By.XPATH,
        #                                             "//*[@id="__next"]/div/div[4]/div[1]/div/div[4]/div/div[6]/div[2]/div[1]/div/div[2]/span/a")
        model_info_element = driver.find_elements(By.XPATH,
                                                    "//div[contains(@class, 'AdParam_adParamContainerVeh__Vz4Zt')].//span[contains(text(), 'Dòng xe:')]//following-sibling::a")
        year_pd_info_element = driver.find_elements(By.XPATH,
                                                    "//div[contains(@class, 'AdParam_adParamContainerVeh__Vz4Zt')].//span[contains(text(), 'Năm sản xuất:')]//span")      
        km_info_element = driver.find_elements(By.XPATH,
                                                  "//div[contains(@class, 'AdParam_adParamContainerVeh__Vz4Zt')].//span[contains(text(), 'Số Km đã đi:')]//span") 
        status_info_element = driver.find_elements(By.XPATH,
                                                  "//div[contains(@class, 'AdParam_adParamContainerVeh__Vz4Zt')].//span[contains(text(), 'Tình trạng:')]//span") 
        transmission_info_element = driver.find_elements(By.XPATH,
                                                  "//div[contains(@class, 'AdParam_adParamContainerVeh__Vz4Zt')].//span[contains(text(), 'Hộp số:')]//span") 
        fuel_info_element = driver.find_elements(By.XPATH,
                                                  "//div[contains(@class, 'AdParam_adParamContainerVeh__Vz4Zt')].//span[contains(text(), 'Nhiên liệu:')]//span")
        country_info_element = driver.find_elements(By.XPATH,
                                                  "//div[contains(@class, 'AdParam_adParamContainerVeh__Vz4Zt')].//span[contains(text(), 'Xuất xứ:')]//span")
        style_info_element = driver.find_elements(By.XPATH,
                                                  "//div[contains(@class, 'AdParam_adParamContainerVeh__Vz4Zt')].//span[contains(text(), 'Kiểu dáng:')]//span")
        seat_capacity_info_element = driver.find_elements(By.XPATH,
                                                  "//div[contains(@class, 'AdParam_adParamContainerVeh__Vz4Zt')].//span[contains(text(), 'Chính sách bảo hành:')]//span")
        payload_info_element = driver.find_elements(By.XPATH,
                                                  "//div[contains(@class, 'AdParam_adParamContainerVeh__Vz4Zt')].//span[contains(text(), 'Trọng lượng:')]//span")
                                      
        #Lấy thông tin từ các thẻ và in r
        # for index, element in enumerate(brand_info_element):
        #         if element.text == 'Hãng:':
        #             if index + 1 < len(brand_info_element):
        #                 brand_element= brand_info_element[index + 1].find_element(By.TAG_NAME, "a")
        #                 brand = brand_element.text
        #             break
        # for index, element in enumerate(brand_info_element.find_elements(By.TAG_NAME, "span")):
        #     if element.text == 'Hãng:':
        #         if index + 1 < len(brand_info_element.find_elements(By.TAG_NAME, "span")):
        #             # Lấy phần tử <a> tiếp theo
        #             brand_element = brand_info_element.find_elements(By.TAG_NAME, "span")[index + 1].find_element(By.TAG_NAME, "a")
        #             brand = brand_element.text
        #         break

        for index, element in enumerate(model_info_element):
                if element.text == 'Dòng xe:':
                    if index + 1 < len(model_info_element):
                        model = model_info_element[index + 1].text
        
        for index, element in enumerate(year_pd_info_element):
                if element.text == 'Năm sản xuất:':
                    if index + 1 < len(year_pd_info_element):
                        year_pd = year_pd_info_element[index + 1].text

        for index, element in enumerate(km_info_element):
                if element.text == 'Số Km đã đi:':
                    if index + 1 < len(km_info_element):
                        km = km_info_element[index + 1].text

        for index, element in enumerate(status_info_element):
                if element.text == 'Tình trạng:':
                    if index + 1 < len(status_info_element):
                        status = status_info_element[index + 1].text

        for index, element in enumerate(transmission_info_element):
                if element.text == 'Hộp số:':
                    if index + 1 < len(transmission_info_element):
                        transmission = transmission_info_element[index + 1].text

        for index, element in enumerate(fuel_info_element):
                if element.text == 'Nhiên liệu:':
                    if index + 1 < len(fuel_info_element):
                        fuel = fuel_info_element[index + 1].text
        
        for index, element in enumerate(country_info_element):
                if element.text == 'Xuất xứ:':
                    if index + 1 < len(country_info_element):
                        country = country_info_element[index + 1].text
        
        for index, element in enumerate(style_info_element):
                if element.text == 'Kiểu dáng:':
                    if index + 1 < len(style_info_element):
                        style = style_info_element[index + 1].text

        for index, element in enumerate(seat_capacity_info_element):
                if element.text == 'Số chỗ:':
                    if index + 1 < len(seat_capacity_info_element):
                        seat_capacity = seat_capacity_info_element[index + 1].text

        for index, element in enumerate(payload_info_element):
                if element.text == 'Trọng tải:':
                    if index + 1 < len(payload_info_element):
                        payload = payload_info_element[index + 1].text
    except:
           return brand,model,year_pd,km,status,transmission,fuel,country,style,seat_capacity,payload
    return brand,model,year_pd,km,status,transmission,fuel,country,style,seat_capacity,payload

def crawl_data(url):
    webdriver_path = "D:\HK6\Tool\msedgedriver.exe"
    service = Service(webdriver_path)
    options = Options()
    driver = webdriver.Edge(service=service, options=options)

    with driver:
        driver.get(url)
        price_real = get_price(driver)
        name = get_name(driver)
        position = get_location(driver)
        brand_ovil = get_brand(driver)
        brand,model,year_pd,km,status,transmission,fuel,country,style,seat_capacity,payload = scrape_data(driver)

        return name,price_real,position,brand_ovil, brand,model,year_pd,km,status,transmission,fuel,country,style,seat_capacity,payload

def main(urls):
    data = []
    url_count = 0
    # Sử dụng context manager để đảm bảo executor được dọn dẹp một cách an toàn
    with ThreadPoolExecutor(max_workers = 10) as executor: # Thay đổi số lượng threads phù hợp với tài nguyên hệ thống
        futures = {executor.submit(crawl_data, url): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            url_count = url_count + 1
            print(len(data), "-", url_count, '/1113')
            try:
                name,price_real,position,brand_ovil,brand,model,year_pd,km,status,transmission,fuel,country,style,seat_capacity,payload = future.result()
                data.append(
                    {'name': name, 'price': price_real, 'position': position, "Brand": brand_ovil,'brand': brand,
                     'model': model,'year_pd': year_pd, 'km': km, 'status': status,
                     'transmission': transmission,'fuel': fuel,'country': country,
                     'style': style, 'seat_capacity': seat_capacity, 'payload': payload})
            except Exception as e:
                print(f"Error crawling {futures[future]}: {e}")
    return data

if __name__ == "__main__":
    # Đọc file CSV chứa danh sách URLs
    df = pd.read_csv('url.csv')

    # Truy cập cột 'URL' trong DataFrame
    urls = df['URL'].tolist()

    start_time = time.time()
    final_data = main(urls)
    end_time = time.time()
    print("Thời gian crawl: ", end_time - start_time, "s")

    df = pd.DataFrame(final_data)

    df.to_csv('data_test.csv', index=False)