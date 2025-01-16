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

# 타입 확인 
def find_type():
    wait = WebDriverWait(driver, 10)
    try:
        # ul 요소가 로드될 때까지 대기
        ul_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sub_container"]/section[2]/div[1]/ul')))
        
        # ul 안의 모든 li 요소 찾기
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")

        # li 요소가 있을 경우 하나씩 클릭
        for index, li in enumerate(li_elements):
            try:
                # a 태그가 존재하는지 확인
                a_tag = li.find_element(By.TAG_NAME, "a") # li 안의 a 태그 찾기
                
                # 클릭 가능한 상태라면 클릭
                if a_tag:
                    a_tag.click()
                    print(f"{index + 1}번째 <li> 텍스트: {a_tag.text} - 클릭")
                    
                    # 클릭 후 잠시 대기 (페이지 로딩 시간 고려)
                    time.sleep(2)  # 필요에 따라 조정
                    
                    # 이전 페이지로 돌아가기 (필요에 따라)
                    driver.back()
                    
                    # 페이지 로드 대기
                    wait.until(EC.presence_of_element_located((By.XPATH, "//ul")))
                else:
                    print(f"{index + 1}번째 <li> 텍스트: {a_tag.text} - 클릭할 수 없음")
            except Exception as e:
                print(f"{index + 1}번째 <li> 처리 중 오류 발생: {e}")
                continue
            
    except Exception as e:
    # ul 요소가 없음
        print("ul 요소 X")
                
# 정보 긁어오기
def info_scrap():
    wait = WebDriverWait(driver, 10)
    
    # 주택이름
    house = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrtancSbdTab0"]/h4[1]')))
    print(house.text)
    # 난방방식
    hiting = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrtancSbdTab0"]/div[1]/div/ul/li[4]')))
    print(hiting.text)
    # 타입
    type = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sub_container"]/section[1]/div[3]/ul/li[2]')))
    print(type.text)
    ## 공급 일정
    # 모집 공고일 
    announcement_date = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sub_container"]/section[1]/div[3]/ul/li[3]')))
    print(announcement_date.text)
    # 공급 일정
    supply_date = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sub_container"]/section[3]/div/ul')))
    print(supply_date.text)
  
# 공고 클릭       
def click_elements():
    wait = WebDriverWait(driver, 10)  # WebDriverWait 설정
    while True:  # 조건에 따라 반복 종료
        try:
            # tbody 요소 가져오기
            tbody = wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
            rows = tbody.find_elements(By.TAG_NAME, "tr")  # 모든 tr 요소 가져오기

            total_rows = len(rows)  # tr 개수 저장
            for index in range(total_rows):  # tr 순회
                try:
                    # tbody와 tr 재조회
                    tbody = wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
                    rows = tbody.find_elements(By.TAG_NAME, "tr")

                    # 현재 index에 해당하는 row 가져오기
                    if index >= len(rows):  # DOM 변경으로 index 초과 방지
                        break

                    row = rows[index]
                    condition_td = row.find_element(By.XPATH, ".//td[2]")  # 조건 <td>
                    text = condition_td.text.strip()

                    if text != "가정어린이집":
                        # 링크 클릭
                        link = row.find_element(By.XPATH, ".//a[contains(@class, 'wrtancInfoBtn')]")
                        link.click()
                        print(f"{index + 1}번째 <tr> 텍스트: {text} - 클릭")

                        # 작업 후 페이지 로딩 대기
                        time.sleep(2)  # 클릭 후 로드 대기 (필요 시 WebDriverWait 대체 가능)
                        find_type()
                        #info_scrap()
                        driver.back()  # 이전 페이지로 이동

                        # 페이지 로드 대기
                        wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
                    else:
                        print(f"{index + 1}번째 <tr> 텍스트: {text} - 클릭하지 않음")
                except Exception as e:
                    print(f"{index + 1}번째 <tr> 처리 중 오류 발생: {e}")
                    continue

            # 작업 완료 후 루프 종료
            break
        except Exception as e:
            print(f"전체 순회 중 오류 발생: {e}")
            break
        
if __name__ == "__main__":
    update_chrome()
    open_page('https://apply.lh.or.kr/lhapply/apply/wt/wrtanc/selectWrtancList.do?mi=1026')
    
    click_elements()
    driver.quit()
    
    