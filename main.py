import time, bs4, urllib, os, urllib.request

from selenium import webdriver
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 초기 셋팅
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.google.co.kr/imghp?hl=ko")
driver.implicitly_wait(3) # 서버가 완전히 로딩 될 때까지 기다림

search_words = list(input('검색할 키워드를 입력해주세요 : ').split('/'))#['무라벨 페트병', '무라벨', '생수병']
for word in search_words:
    print(f'-------------- {word} --------------')
    # 검색
    print(f'[!] "{word}" 검색합니다.')
    elem = driver.find_element(By.NAME, "q")
    elem.clear()
    elem.send_keys(word)
    elem.send_keys(Keys.RETURN)
    SCROLL_PAUSE_TIME = 1

    # 파일 생성
    try:
        if not os.path.exists(f'./{word}_img_download'):
            print(f'[!] "{word}" 파일을 생성합니다.')
            os.makedirs(f'./{word}_img_download')
    except OSError:
        print(f'Error: Creating directory. ./{word}_img_download')

    # 스크롤
    print(f'[!] "{word}" 스크롤중입니다...')
    elem = driver.find_element(By.TAG_NAME, "body")
    for i in range(60):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    
    # 이미지 추출
    print(f'[!] "{word}" 이미지 정보를 받고있습니다...')
    links = []
    images = driver.find_elements(By.CSS_SELECTOR, '.YQ4gaf')
    for image in images:
        if image.get_attribute('src') != None:
            links.append(image.get_attribute('src'))
    print(f'"{word}" 찾은 이미지 개수: {len(links)}')
    print()
    time.sleep(2)

    print(f'[!] 이미지 다운로드를 시작합니다.')
    for k, i in enumerate(links):
        url = i
        start = time.time()
        urllib.request.urlretrieve(url, "./"+word+"_img_download/"+word+"_"+str(k)+".jpg")
        print(f'{str(k+1)}/{str(len(links))} {word} 다운로드 중...... Download time : {str(time.time()-start)[:5]} 초')
    print(f'[!] "{word}" 다운로드 완료')
    print()
driver.quit()
