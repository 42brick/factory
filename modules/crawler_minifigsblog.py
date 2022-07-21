import os
import time
import platform
from datetime import date
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import urllib
from urllib.request import urlopen
from urllib.parse import quote_plus

# 1. 드라이버 로드
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-sdev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"
#chrome_options.add_argument('--window-size=1920,1080')

# 2. OS 에 맞춰 드라이버 세팅 (버전 체크 필요)
if platform.system() == 'Windows': 
	# driver_link = os.getcwd() + '/factory/modules/driver/chromedriver.exe'
	driver_link = "C:/chromedriver.exe"
else:
	driver_link = os.getcwd() + '/factory/modules/driver/chromedriver_m1'
driver = webdriver.Chrome(driver_link, options=chrome_options)


# 3. 테마 내 미니피규어 이미지 찾기
def find_lego(url: str, cnt: int) -> list:
    driver.get(url)
    minifigs_url = []
    minifigs_serial = []

    # 테마 당 미니피규어 개수 체크
    for i in range(0, cnt):
        if i < 21: # 20까지는 동일한 페이지 내에 존재하는 이미지 수집
            driver.refresh()
            time.sleep(1)

            xpath = '//*[@id="primary"]/ul/li' + "[{idx}]".format(idx = str(i+1)) + '/div[1]/a'
            img_container = driver.find_element(by=By.XPATH, value=xpath)
            img_container.click()
            driver.switch_to.frame(0)

            second_img_path = '/html/body/div[2]/div[1]/img[1]' # 정면을 바라보고 있는 이미지 수집
            lego = driver.find_element(by=By.XPATH, value=second_img_path)
            lego = lego.get_attribute('src')
            serial = driver.current_url.split('-')[-1][:-1]

            if 'yeti' in str(serial):
                serial = 'col170'

            minifigs_url.append(lego) # 이미지 경로
            minifigs_serial.append(serial)

            driver.back()
            time.sleep(1)

        elif i >= 21 and i % 21 == 0:
            driver.refresh()
            time.sleep(1)

            #ul의 마지막 자식 노드를 탐색(>)
            next_num = '/html/body/div[1]/div/div/div[1]/nav/ul/li[last()]/a'
            try:
                page_next = driver.find_element(by=By.XPATH, value=next_num)
            except:
                break
            page_next.click()

            xpath = '//*[@id="primary"]/ul/li' + "[{idx}]".format(idx = str(i % 21 + 1)) + '/div[1]/a'
            img_container = driver.find_element(by=By.XPATH, value=xpath)
            img_container.click()
            driver.switch_to.frame(0)

            second_img_path = '/html/body/div[2]/div[1]/img[1]' #정면을 바라보고 있는 이미지 수집
            lego = driver.find_element(by=By.XPATH, value=second_img_path)
            lego = lego.get_attribute('src')
            serial = driver.current_url.split('-')[-1][:-1]
            minifigs_url.append(lego) #이미지 경로
            minifigs_serial.append(serial)

            driver.back()
            time.sleep(1)
        
        else:
            driver.refresh()
            time.sleep(1)

            xpath = '//*[@id="primary"]/ul/li' + "[{idx}]".format(idx = str(i % 21 + 1)) + '/div[1]/a'
            img_container = driver.find_element(by=By.XPATH, value=xpath)
            img_container.click()
            driver.switch_to.frame(0)

            second_img_path = '/html/body/div[2]/div[1]/img[1]' #정면을 바라보고 있는 이미지 수집
            lego = driver.find_element(by=By.XPATH, value=second_img_path)
            lego = lego.get_attribute('src')
            serial = driver.current_url.split('-')[-1][:-1]

            minifigs_url.append(lego) #이미지 경로
            minifigs_serial.append(serial)

            driver.back()
            time.sleep(1)

    driver.back()
    time.sleep(1)
    return minifigs_url, minifigs_serial

def main():
    base_url = 'https://minifigs.blog/collection'
    driver.get(base_url)

    #카테고리 별로 나누기
    category = driver.find_elements(by=By.CLASS_NAME, value='cat-item')
    category_list = []
    category_cnt = []
    for li in category:
        cat = li.find_element(by=By.TAG_NAME, value='a').text
        cnt_text = li.find_element(by=By.TAG_NAME, value='span').text
        cnt = int(cnt_text.strip('()'))
        category_list.append(cat)
        category_cnt.append(cnt)


    for cat, cnt in zip(category_list[7:9], category_cnt[7:9]): # 테마 범위 설정 슬라이싱
        collectible = ['Avengers Infinity War', 'DC Super Heroes', 'Jurassic World', 'Other', 'Unikitty']

        # page 변동으로 예외 다수
        if cat == 'Collectible Minifigures' or cat == 'Stormtroopers':
            continue

        elif cat == 'Batman I':
            theme = 'batman-1'
            category_url = 'https://minifigs.blog/product-category/collectible/'

        elif cat == 'Other':
            theme = 'col-other'
            category_url = 'https://minifigs.blog/product-category/'

        elif cat == 'Series 19':
            theme = 'series-19'
            category_url = 'https://minifigs.blog/product-category/collectible/'

        elif cat != 'Disney Series 2' and 'Series' in cat:
            theme = cat.lower().strip().replace(' ', '_')
            category_url = 'https://minifigs.blog/product-category/collectible/'

        elif cat not in collectible and 'Series' not in cat and 'The LEGO' not in cat: # category:collectible 체크 조건
            theme = cat.lower().strip().replace(' ', '-')    
            category_url = 'https://minifigs.blog/product-category/'

        else:
            theme = cat.lower().strip().replace(' ', '-')
            category_url = 'https://minifigs.blog/product-category/collectible/'
            
        minifigs_url, minifigs_serial = find_lego(category_url+theme, cnt)
        
        if platform.system() == 'Windows':
            if not os.path.exists(f"C:/SGM_AI/42Brick/factory/img_blog/{theme}"):
                os.makedirs(f"C:/SGM_AI/42Brick/factory/img_blog/{theme}")
        else:
            if not os.path.exists(os.getcwd() + f"/factory/img_blog/{theme}"):
                os.makedirs(os.getcwd() + f"/factory/img_blog/{theme}")
                
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        for url, serial in zip(minifigs_url, minifigs_serial):
            urllib.request.urlretrieve(url, "C:/SGM_AI/42Brick/factory/img_blog/{0}/{1}.jpg".format(theme, serial))


if __name__ == "__main__":
    main()