from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import pandas as pd
import re
# Tạo dataframe rỗng
d = pd.DataFrame({'name': [], 'birth': [], 'death': [], 'nationality': []})
#khởi tạo Webdriver
driver = webdriver.Chrome()

url = "https://en.wikipedia.org/wiki/Edvard_Munch"


# mở trang

driver.get(url)

# đợi khoảng chừng 2s
time.sleep(2)

try:
    name = driver.find_element(By.TAG_NAME, "h1").text
except:
    name = ""

#lấy ngày sinh
try:
    birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
    birth = birth_element.text
    birth = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', birth)[0]
except:
    birth = ""
#lấy ngày mất
try:
    death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
    death = death_element.text
    death = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', death)[0]
except:
    death = ""
#
try:
    nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
    nationality = nationality_element.text
except:
    nationality = ""
#tạo dictionary  thong tin của họa sĩ
painter = {'name': name, 'birth': birth, 'death': death, 'nationality': nationality}

painter_df = pd.DataFrame([painter])

d = pd.concat([d, painter_df], ignore_index=True)

print(d)
# đóng webdriver
driver.quit()
