from selenium import webdriver
from selenium.webdriver.common.by import By
import time
#khởi tạo Webdriver
driver = webdriver.Chrome()

#mở trang
url = "https://en.wikipedia.org/wiki/List_of_painters_by_name"

driver.get(url)

#đợi khoảng chừng 2s
time.sleep(2)

# lấy tất cả các thẻ <a: các thẻ mình có thể click chuột> với title chứa "list of painters
tags = driver.find_elements(By.XPATH, "//a[contains(@title , 'List of painters')]")
#lấy nhưngx đường link nòa chỉ chứa sp mình cần
# tạo ra danh sách các liên kết lấy từng cái đường hr thẻ ở trong tag
links = [tag.get_attribute("href")for tag in tags]

#xuất thông tin
for link in links:
    print(link)

# đóng webdriver
driver.quit()