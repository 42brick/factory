from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date

def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


# 1. 드라이버 로드
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('./chromedriver', options=chrome_options)


def parsing(webdriver, url):
    webdriver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    return soup


if __name__ == "__main__":
    base_url = 'https://www.brickeconomy.com/minifigs'
    soup = parsing(webdriver, base_url)
    theme_parse = soup.find_all("div", {"class":"theme"})
    theme_list = [theme.find("a").get_text() for theme in theme_parse]
    driver.close()

    for theme in theme_list:
        theme_url = base_url + f"/theme/{theme}"
        soup = parsing(driver, base_url + theme_url)


# 2. 세부내역 확인

# 범위
# /html/body/form/div[2]/div/div/div[2]/div[1]/div/div/div[1]
# /html/body/form/div[2]/div/div/div[2]/div[1]/div/div/div[125]
#
# /html/body/form/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[1]/a