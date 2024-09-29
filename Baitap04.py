from selenium import webdriver
from selenium.webdriver.common.by import By
import time
#khởi tạo Webdriver
driver = webdriver.Chrome()
for i in range(65, 91):
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22"+chr(i)+"%22"

    try:
        # mở trang

        driver.get(url)

        # đợi khoảng chừng 2s
        time.sleep(2)

        # lấy tất cả các thẻ ul
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")


        # chọn thẻ ul thứ 21
        ul_painters = ul_tags[20]  # list start with imdex =0

        # lấy ra tất cả thẻ <li> thuọc ul_painters
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

        # tạo danh sách các url
        titles = [tag.find_element(By.TAG_NAME, "a").get_attribute("title") for tag in li_tags]

        # xuất thông tin

        for title in titles:
            print(title)

    except:
        print("Error")



# đóng webdriver
driver.quit()
