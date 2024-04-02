from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

webdriver_path = "D:\HK6\Tool\msedgedriver.exe"
service = Service(webdriver_path)
options = Options()

driver = webdriver.Edge(service=service, options=options)

url = "https://xe.chotot.com/mua-ban-oto-quan-8-tp-ho-chi-minh?page=2"

driver.get(url)

time.sleep(15)
elements = driver.find_elements(By.XPATH, "//div[@role='button']//following-sibling::a")
url_sp = []

existing_df = pd.read_csv("urls.csv")

for element in elements:
    # Lấy giá trị của thuộc tính href
    href_value = element.get_attribute("href")
    url_sp.append(href_value)

print(len(url_sp))

driver.quit()

df = pd.DataFrame(url_sp, columns=["URL"])
combined_df = pd.concat([existing_df, df], ignore_index=True)

# Lưu DataFrame thành tệp CSV
combined_df.to_csv("urls.csv", index=False)