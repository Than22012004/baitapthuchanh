import string
import re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Cấu hình Chrome để chạy nền (headless)
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--headless")  # Nếu bạn muốn chạy headless

# Khởi tạo DataFrame rỗng để chứa thông tin họa sĩ
d = pd.DataFrame({'name': [], 'birth': [], 'death': [], 'nationality': []})


# Hàm lấy thông tin từng họa sĩ
def get_painter_info(link):
    try:
        # Khởi tạo webdriver
        driver = webdriver.Chrome(options=chrome_options)

        # Mở trang
        driver.get(link)

        # Đợi trang tải và đảm bảo thẻ <h1> (tên họa sĩ) xuất hiện
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

        # Lấy tên họa sĩ
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        # Lấy ngày sinh
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', birth_element.text)[0]
        except:
            birth = ""

        # Lấy ngày mất
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death = re.findall(r'[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}', death_element.text)[0]
        except:
            death = ""

        # Lấy quốc tịch
        try:
            nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
            nationality = nationality_element.text
        except:
            nationality = ""

        # Tạo dictionary chứa thông tin họa sĩ
        painter = {'name': name, 'birth': birth, 'death': death, 'nationality': nationality}

        return painter

    except Exception as e:
        print(f"Lỗi khi truy cập {link}: {e}")
        return None

    finally:
        # Đóng driver trong mọi trường hợp
        driver.quit()


# Hàm lấy danh sách liên kết đến trang họa sĩ từ trang danh sách theo chữ cái
def get_painter_links_by_letter(letter):
    links = []
    driver = webdriver.Chrome(options=chrome_options)
    url = f"https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22{letter}%22"

    try:
        driver.get(url)

        # Đợi trang tải đầy đủ và kiểm tra số lượng thẻ <ul>
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "ul")))

        # Lấy tất cả các thẻ <ul>
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        max_li_count = 0
        ul_painters = None

        # Tìm thẻ <ul> có nhiều <li> nhất, giả định đây là danh sách họa sĩ
        for ul in ul_tags:
            li_tags = ul.find_elements(By.TAG_NAME, "li")
            if len(li_tags) > max_li_count:
                max_li_count = len(li_tags)
                ul_painters = ul

        if ul_painters:
            # Lấy tất cả liên kết của các họa sĩ
            li_tags = ul_painters.find_elements(By.TAG_NAME, "li")
            for li in li_tags:
                try:
                    a_tag = li.find_element(By.TAG_NAME, "a")
                    link = a_tag.get_attribute("href")
                    if "/wiki/" in link:  # Chỉ lấy các liên kết đến Wikipedia
                        links.append(link)
                except:
                    continue

    except Exception as e:
        print(f"Lỗi khi truy cập trang {letter}: {e}")

    finally:
        driver.quit()

    return links


# Sử dụng ThreadPoolExecutor để thu thập thông tin song song
for letter in string.ascii_uppercase:  # Duyệt qua các chữ cái từ A đến Z
    print(f"Đang xử lý các họa sĩ bắt đầu với '{letter}'")
    painter_links = get_painter_links_by_letter(letter)
    print(f"Thu thập được {len(painter_links)} họa sĩ cho '{letter}'")

    # Sử dụng ThreadPoolExecutor để xử lý các liên kết song song
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(get_painter_info, painter_links))

    # Thêm các kết quả vào DataFrame
    for painter in results:
        if painter:
            d = pd.concat([d, pd.DataFrame([painter])], ignore_index=True)

# Lưu kết quả vào file Excel
file_name = 'Painters_All_World.xlsx'
d.to_excel(file_name, index=False)
print('DataFrame đã được ghi vào file Excel thành công.')
