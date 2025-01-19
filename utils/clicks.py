from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import re

from utils.find_type import find_type
from utils.basic_scrap import basic_info_scrap

# 공고 클릭       
def click_elements(driver):
    wait = WebDriverWait(driver, 10)  # WebDriverWait 설정
    clicked_links = set()  # 클릭한 링크 추적
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
                        link_name = re.sub(r'[^A-Za-z0-9가-힣ㄱ-ㅎㅏ-ㅣ\s\-]', '_', link.text).replace(' ', '_')
                        
                        if link_name not in clicked_links:
                            clicked_links.add(link_name)
                            link.click()
                            print(f"{index + 1}번째 {link_name} - 클릭")    
                            time.sleep(2)  # 클릭 후 로드 대기  

                            target_file, link_name = basic_info_scrap(driver, f'{link_name}.json') # 기본 정보 가져오기         
                            time.sleep(2)  # 클릭 후 로드 대기 

                            find_type(driver, target_file, link_name) # 타입 검사
                            time.sleep(2)  # 클릭 후 로드 대기 
                            driver.back()  # 이전 페이지로 이동
                            wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))  # 뒤로 간 후 로딩 대기
                        else:
                            print(f"{index + 1}번째 {link_name} - 이미 클릭됨")
                    else:
                        print(f"{index + 1}번째 <tr> 텍스트: {link_name} - 클릭 X")
                except Exception as e:
                    print(f"{index + 1}번째 <tr> 처리 중 오류 발생: {e}")
                    continue

            # 작업 완료 후 루프 종료
            print("모든 항목 처리 완료!")
            break
        except Exception as e:
            print(f"전체 순회 중 오류 발생: {e}")
            break
