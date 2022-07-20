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
#chrome_options.add_argument('--window-size=1920,1080')
if platform.system() == 'Windows': #크롬 드라이버 확인
	# driver_link = os.getcwd() + '/factory/modules/driver/chromedriver.exe'
	driver_link = "C:/chromedriver.exe"
else:
	driver_link = os.getcwd() + '/factory/modules/driver/chromedriver_m1'
driver = webdriver.Chrome(driver_link, options=chrome_options)

def parsing():
	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")
	return soup


def find_lego(idx):
	xpath = f'/html/body/form/div[2]/div/div/div[2]/div[1]/div/div/div[{idx}]/div[1]'
	first_xpath = xpath + '/a'
	img_container = driver.find_element(by=By.XPATH, value=first_xpath)
	theme = img_container.get_attribute('href').split('/')[-1]
	img_container.click()

	#중분류 미니피규어 개수
	minifigs_num = driver.find_element(by=By.XPATH, value='/html/body/form/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]').text

	soup = parsing()
	minifigs_serial = []
	if soup.find("div", {"class":"paging"}):
		minifigs_serial.extend([td.find("a")['href'].split('/')[-2] for td in soup.find_all("td", {"class":"ctlminifigs-image"})])
		next_btn_idx = len(soup.find_all("li", {"class":"page-item"})) - 1
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

	driver.back()
	time.sleep(1)
	return theme, minifigs_serial


if __name__ == "__main__":

	base_url = 'https://www.brickeconomy.com/minifigs'
	driver.get(base_url)
	for i in range(1, 126):
		minifigs = []
		theme, minifigs_serial = find_lego(i) #1~125
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

		for ele in minifigs:
			img = 'https://www.brickeconomy.com/resources/images/minifigs/' + ele + '_large.jpg'
			urllib.request.urlretrieve(img, "C:/SGM_AI/42Brick/factory/img/{0}/{1}.jpg".format(theme, ele))

	"""
	1. /html/body/form/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[1]/a 를 클릭한다
	// 2. 받은 값을 공백은 -로 replace, 나머지는 lowercase() - 속도 측면일뿐, 안해주는게 나을듯
	3. 이렇게 1부터 125까지 돌아간다. 범위는 아래 참고
	4. https://www.brickeconomy.com/minifigs/theme/중분류 접속
	5. 페이지 당 미니피규어 개수 체크, 위치는 /html/body/form/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]의 값
	6. 각 미니피규어의 시리얼 넘버 체크
	형식은 : /html/body/form/div[2]/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[2]/td[2]/div[2]
	5. 이렇게 얻은 시리얼 넘버를 https://www.brickeconomy.com/resources/images/minifigs/js028_large.jpg
	 https://www.brickeconomy.com/resources/images/minifigs/ + serial_num + _large.jpg
	"""

# 범위
# /html/body/form/div[2]/div/div/div[2]/div[1]/div/div/div[1]
# /html/body/form/div[2]/div/div/div[2]/div[1]/div/div/div[125]

#결국 최종적으로 필요한 것은 https://www.brickeconomy.com/resources/images/minifigs/js028_large.jpg 이 url

#요게 이미지 있는 url /html/body/form/div[2]/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[2]/td[2]/div[2]