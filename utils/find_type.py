from selenium.webdriver.common.by import By
import time

from utils.detail_scrap import detail_info_scrap

# 타입 확인 
def find_type(driver, target_file, link_name):
    try:
        ul_xpath = '//*[@id="sub_container"]/section[2]/div[1]/ul'

        # 해당 ul 안에 있는 li 요소들의 XPath를 찾을 수 있습니다.
        li_elements = driver.find_elements(By.XPATH, f"{ul_xpath}/li")
        
        # li 요소가 없을 때 메시지 출력
        if not li_elements:
            print("type X")
            time.sleep(2)  # 클릭 후 로드 대기 
            detail_info_scrap(driver, target_file, link_name, 0)
            time.sleep(2)  # 클릭 후 로드 대기 
            return

        # 각 li의 텍스트 출력
        cnt = 0
        for li in li_elements:
            try:
                # li 안에 있는 a 태그 찾기
                a_tag = li.find_element(By.TAG_NAME, "a")
                
                # a 태그가 존재하면 클릭
                if a_tag:
                    a_tag.click()
                    print(f"type {cnt+1}번: {a_tag.text} 클릭됨")
                    time.sleep(2)  # 클릭 후 로드 대기 
                    detail_info_scrap(driver, target_file, link_name, cnt)
                    time.sleep(2)  # 클릭 후 로드 대기 
                    cnt += 1
                    time.sleep(2)  # 클릭 후 잠시 대기 (필요에 따라 조정)
            except Exception as e:
                print(f"li 클릭 중 오류 발생: {e}")

    except Exception as e:
        print(f"오류 발생: {e}")  # 그 외의 예외 처리