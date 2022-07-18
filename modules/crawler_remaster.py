import platform
from selenium import webdriver
from datetime import date
import time
import os
import urllib
from urllib.request import urlopen
from urllib.parse import quote_plus
from selenium.webdriver import ActionChains

# 1. 드라이버 로드
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-sdev-shm-usage')
chrome_options.add_argument('--disable-gpu')
#chrome_options.add_argument('--window-size=1920,1080')
if platform.system() == 'Windows': #크롬 드라이버 확인
    driver_link = 'C:/Users/waudy/Desktop/factory/factory/modules/driver/chromedriver.exe'
else:
    driver_link = 'C:/Users/waudy/Desktop/factory/factory/modules/driver/chromedriver_mac64'
driver = webdriver.Chrome(driver_link, options=chrome_options)

def find_lego(idx):
    xpath = '/html/body/form/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[' + str(idx) + ']'
    first_xpath = xpath + '/a'
    img_container = driver.find_element_by_xpath(first_xpath)
    img_container.click()
    
    #중분류 미니피규어 개수
    minifigs_num = driver.find_element_by_xpath('/html/body/form/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]').text
    
    if int(minifigs_num) > 50: #여기서 pagination이 있는 경우에만 체크를 진행한다. 골격만 남겨둠
        minifigs_num = 50 #pagination 미진행

    minifigs_serial = [] #현재 중분류 레고의 시리얼 번호만 담기
    for serial_idx in range(2, int(minifigs_num) * 2, 2):
        serial_path = '/html/body/form/div[2]/div[2]/div[1]/div[2]/div[2]/table/tbody/tr['+ str(serial_idx) + ']/td[2]/div[2]' #2, 4, 6의 형식으로 긁는다
        serial = driver.find_element_by_xpath(serial_path).text[15:] #Minifig Number \부분제외
        minifigs_serial.append(serial)
    
    minifigs.extend(minifigs_serial) #나중에 key:value pair로 저장 방식 채택 가능_중분류:시리얼 넘버
    driver.back()
    time.sleep(1)
    action = ActionChains(driver)
    next_xpath = driver.find_element_by_xpath('/html/body/form/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[' + str(idx + 1) + ']')
    action.move_to_element(next_xpath).perform() #필요한 만큼 페이지 단위로 끊어서 내려가는 작업 필요

    

if __name__ == "__main__":
    base_url = 'https://www.brickeconomy.com/minifigs'
    driver.get(base_url)
    minifigs = []
    for i in range(1, 126):
        find_lego(i) #1~125

    if not os.path.exists("C:/Users/waudy/Desktop/factory/img"):
        os.makedirs("C:/Users/waudy/Desktop/factory/img")

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    for ele in minifigs:
        img = 'https://www.brickeconomy.com/resources/images/minifigs/' + ele + '_large.jpg'
        urllib.request.urlretrieve(img, "C:/Users/waudy/Desktop/factory/img/{0}.jpg".format(ele))
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