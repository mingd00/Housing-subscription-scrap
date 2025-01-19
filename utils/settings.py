from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import shutil
import json
import os

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
    return driver
    
# 페이지 열기
def open_page(page_url):
    driver.get(page_url)
    
# json 파일 복사
def create_json(new_file):
    file_path = os.path.join('json', new_file)
    shutil.copy('format.json', file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        new_json = json.load(f)
    return new_json

# JSON 파일에 데이터를 저장하는 함수
def save_json(target_json, file_name):
    file_path = os.path.join('json', file_name)  
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(target_json, f, ensure_ascii=False, indent=4)
    