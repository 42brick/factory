import platform
from selenium import webdriver
from datetime import date
import time
import os
import urllib
from urllib.request import urlopen
from urllib.parse import quote_plus
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

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

# 3. html 파싱 세팅
def parsing():
	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")
	return soup

# 4. 페이지 내 미니피규어 이미지 찾기
def find_lego(idx):
	xpath = f'/html/body/form/div[2]/div/div/div[2]/div[1]/div/div/div[{idx}]/div[1]/a' # brickeconomy 중분류
	img_container = driver.find_element(by=By.XPATH, value=xpath)
	theme = img_container.get_attribute('href').split('/')[-1]
	img_container.click()

	soup = parsing()
	minifigs_serial = []
	# 5. page 가 나뉘어져 있는지 확인
	if soup.find("div", {"class":"paging"}):
		minifigs_serial.extend([td.find("a")['href'].split('/')[-2] for td in soup.find_all("td", {"class":"ctlminifigs-image"})])
		next_btn_idx = len(soup.find_all("li", {"class":"page-item"}))
		while True:
			next_btn = driver.find_element(by=By.XPATH, value=f"/html/body/form/div[2]/div[2]/div[1]/div[2]/div[3]/ul/li[{next_btn_idx}]/a")
			try:
				next_btn.click()
				time.sleep(1)
				soup = parsing()
				if [td.find("a")['href'].split('/')[-2] for td in soup.find_all("td", {"class":"ctlminifigs-image"})][0] in minifigs_serial:
					break
				minifigs_serial.extend([td.find("a")['href'].split('/')[-2] for td in soup.find_all("td", {"class":"ctlminifigs-image"})])
			except:
				break
	else:
		minifigs_serial.extend([td.find("a")['href'].split('/')[-2] for td in soup.find_all("td", {"class":"ctlminifigs-image"})])

	print(theme,minifigs_serial)
	driver.back()
	time.sleep(1)
	return theme, minifigs_serial

def main():
	base_url = 'https://www.brickeconomy.com/minifigs'
	driver.get(base_url)

	for i in range(1, 126):
	# sports(95번), start-wars(96번), town(113번)에서 오류 발생
	# for i in [95, 96, 113]:
		minifigs = []
		theme, minifigs_serial = find_lego(i) #1~125, 중분류 개수
		minifigs.extend(minifigs_serial)

		if platform.system() == 'Windows':
			if not os.path.exists(f"C:/SGM_AI/42Brick/factory/img/{theme}"):
				os.makedirs(f"C:/SGM_AI/42Brick/factory/img/{theme}")
		else:
			if not os.path.exists(os.getcwd() + f"/factory/img/{theme}"):
				os.makedirs(os.getcwd() + f"/factory/img/{theme}")

		opener = urllib.request.build_opener()
		opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
		urllib.request.install_opener(opener)

		for e in minifigs:
			img = 'https://www.brickeconomy.com/resources/images/minifigs/' + e + '_large.jpg'
			urllib.request.urlretrieve(img, "C:/SGM_AI/42Brick/factory/img/{0}/{1}.jpg".format(theme, e))


if __name__ == "__main__":
	main()
