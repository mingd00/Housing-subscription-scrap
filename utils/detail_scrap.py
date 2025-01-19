from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import time

from utils.settings import save_json

# 세부 정보 긁어오기
def detail_info_scrap(driver, target_file, link_name, tab):
    wait = WebDriverWait(driver, 10)
    
    # 주택 이름
    house = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="wrtancSbdTab{tab}"]/h4[1]'))).text
    
    # 주택 주소
    location = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="wrtancSbdTab{tab}"]/div[1]/div/ul/li[1]'))).text[6:]
    
    # 난방 방식
    hiting = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="wrtancSbdTab{tab}"]/div[1]/div/ul/li[4]'))).text[7:]
    
    # 주택 유형 안내 
    theads = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#wrtancSbdTab{tab} > div.tbl_st.tbl_rsp.tyCross.tymBtn.tblmobToge > table > thead')))  
    th_elements = theads.find_elements(By.TAG_NAME, "th") 
    
    # 이미지(위치도, 단지조감도, 단지배치도)
    try:
        # 요소가 있는지 검사
        wait = WebDriverWait(driver, 10)
        ul_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#wrtancSbdTab{tab} > div.tab_st03_1.tabDom.Tab_w20 > ul')))

        while True:
            # ul 안의 모든 li 요소들 찾기
            li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
            
            # 각 li 요소를 클릭
            for li in li_elements:
                print(f"클릭할 요소: {li.text}")
                li.click()
            
    except Exception as e:
        print("사진 X")
    
    # 조건을 만족하는 <th> 태그의 인덱스 찾기
    matching_indices = {}
    for index, th in enumerate(th_elements):
        th_text = th.text.strip()  # 텍스트를 추출하고 공백 제거
        if "전용면적" in th_text:
            matching_indices["전용면적"] = index
        elif "금회공급" in th_text:
            matching_indices["금회공급"] = index

    units = []
    types = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#wrtancSbdTab{tab} > div.tbl_st.tbl_rsp.tyCross.tymBtn.tblmobToge > table > tbody')))
    rows = types.find_elements(By.TAG_NAME, "tr")  # tbody 내의 모든 tr 요소 찾기
    
    for row in rows:
        txt = row.find_elements(By.XPATH, ".//th")[0].text  # 각 tr 내에서 th 요소 찾기
        # 닫히지 않은 괄호를 처리
        if txt.count('(') > txt.count(')'):
            txt += ')'  # 부족한 닫는 괄호 추가

        # 괄호 여부를 확인한 후 처리
        if '(' in txt and ')' in txt:  # 괄호가 있는 경우
            # 괄호 전 텍스트 추출
            type_text = txt[:txt.index('(')].strip()

            # 괄호 안 텍스트 추출
            inner_text = txt[txt.index('(') + 1:-1]

            # 괄호 안 텍스트를 확인하고 처리
            if '(' in inner_text:  # 중첩 괄호가 있을 경우
                main_context_match = re.match(r'^(.*)\((.*)\)$', inner_text)
                if main_context_match:
                    main_context = main_context_match.group(1).strip()  # 메인 컨텍스트
                    sub_items = [item.strip() for item in main_context_match.group(2).split(',')]  # 쉼표로 분리된 값들
                    eligible_residents = [f"{item}({main_context})" for item in sub_items]
                else:
                    eligible_residents = [inner_text.strip()]  # 기본 처리 (에러 방지)
            else:  # 중첩 괄호가 없을 경우
                eligible_residents = [item.strip() for item in inner_text.split(',')]  # 쉼표로 분리된 리스트로
        else:  # 괄호가 없는 경우
            type_text = txt.strip()  # 전체를 type_text로 처리
            eligible_residents = None
                
        tds = row.find_elements(By.XPATH, ".//td")  # 각 tr 내에서 td 요소 찾기
        units.append({
            "type": type_text,
            "eligible_residents": eligible_residents,
            "current_supply": tds[matching_indices["금회공급"]-1].text,
            "exclusive_area_m2": tds[matching_indices["전용면적"]-1].text,
            "images": None
            })

    complex_data = {
        "complex_name": house,
        "location": location,
        "heating": hiting,
        "units": units,
        "house_images": {
            "location_map": None,
            "complex_overview": None,
            "complex_site_plan": None,
            "unit_layout_plan": None
        }
    }
    
    target_file['complex_info'].append(complex_data)
    save_json(target_file, link_name)
