from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time
import json

# 드라이버 업데이트
def update_chrome():
    global driver
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('lang=ko_KR')
    chrome_options.add_argument('disable-gpu')
    # chrome_options.add_argument("headless")
    chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
# 페이지 열기
def open_page(page_url):
    driver.get(page_url)

def create_json_file(result_data):
    with open("image_url.json", "w", encoding="utf-8") as json_file:
        json.dump(result_data, json_file, indent=4, ensure_ascii=False)

# 유형에 분양, 임대, 주택이 포함되면 클릭 
def click_if_keyword_present():
    # 특정 클래스명이 적용된 td 요소들을 찾기
    td_elements = driver.find_elements(By.CSS_SELECTOR, 'td.mVw.cate.col1')

    # 각 td 요소에서 텍스트 확인 후, 조건에 맞으면 클릭하고 다시 돌아오기
    for td in td_elements:
        text = td.text.strip()  # 텍스트 가져오기 및 공백 제거
        print(text)
        if any(keyword in text for keyword in ["분양", "임대", "주택"]):
            td.click()  # 클릭
            break

def info_scrap(cnt):
    hiting = driver.find_element(By.CSS_SELECTOR, f"#wrtancSbdTab{str(cnt)} > div.box_st4 > div > ul > li:nth-child(4)")
    print(hiting.text)

def find_type():
    # ul 요소 찾기
    ul_element = driver.find_element(By.CSS_SELECTOR, "#sub_container > section:nth-child(20) > div.tab_st01_1.tabDom.Tab_w20 > ul")
    # ul 내의 자식 요소(예: li) 찾기
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    # 각 li 요소에서 a 태그를 찾아 클릭
    cnt = 0
    for li in li_elements:
        try:
            
            a_element = li.find_element(By.TAG_NAME, "a") # li 안의 a 태그 찾기
            
            print(f"타입: {a_element.text}")  # 링크 텍스트 출력
           
            a_element.click()  # 링크 클릭
            
            # 클릭 후 필요한 작업(예: 페이지 로드 기다리기) 추가 가능
            info_scrap(cnt)
            cnt += 1
            
        except Exception as e:
            print(f"오류 발생: {e}")
        
if __name__ == "__main__":
    update_chrome()
    open_page('https://apply.lh.or.kr/lhapply/apply/wt/wrtanc/selectWrtancList.do?mi=1026')
    
    click_if_keyword_present()
    find_type()
    
    