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
    try:
        ul_xpath = '//*[@id="sub_container"]/section[2]/div[1]/ul'

        # 해당 ul 안에 있는 li 요소들의 XPath를 찾을 수 있습니다.
        li_elements = driver.find_elements(By.XPATH, f"{ul_xpath}/li")

        # 각 li의 텍스트 출력
        for li in li_elements:
            try:
                # li 안에 있는 a 태그 찾기
                a_tag = li.find_element(By.TAG_NAME, "a")
                
                # a 태그가 존재하면 클릭
                if a_tag:
                    a_tag.click()
                    print(f"{a_tag.text} 클릭됨")
                    time.sleep(2)  # 클릭 후 잠시 대기 (필요에 따라 조정)
            except Exception as e:
                print(f"li 클릭 중 오류 발생: {e}")
            
    except NoSuchElementException as e:
        print("ul 요소가 존재하지 않습니다.")  # ul이 없을 때 처리
    except Exception as e:
        print(f"오류 발생: {e}")  # 그 외의 예외 처리
                
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
    
    