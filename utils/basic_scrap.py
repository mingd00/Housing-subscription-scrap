from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

from utils.settings import create_json, save_json

# 정규 표현식 날짜 추출
def cal_date(text, period=True):
    dates = re.findall(r'\d{4}\.\d{2}\.\d{2}', text)
    
    # 하루 추출 
    if period == False:
        if len(dates) > 0:
            formatted_dates = dates[0].replace('.', '-')
        else:
            formatted_dates = None
        return formatted_dates
    
    # 기간 추출 
    if len(dates) == 2:
        formatted_dates = [date.replace('.', '-') for date in dates]
    elif len(dates) == 1:
        formatted_dates = [dates[0].replace('.', '-')] * 2  # 1개일 때 동일한 날짜로 두 번 추가
    else:
        formatted_dates = None
        
    return formatted_dates
    
# 기본 정보 긁어오기
def basic_info_scrap(driver, link_name):
    wait = WebDriverWait(driver, 10)
    # json 포맷 복사
    target_file = create_json(link_name)
    
    # 유형
    house_type = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sub_container"]/section[1]/div[3]/ul/li[2]')))
    target_file['house_type'] = house_type.text[2:]
    
    # 공고일
    announcement_date = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sub_container"]/section[1]/div[3]/ul/li[3]')))
    target_file['schedule']['announcement_date'] = cal_date(announcement_date.text, period=False)
    
    
    # 공급 일정
    supply_schedule = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sub_container"]/section[3]')))
    section_keywords = {
        "접수기간": "application_period",
        "서류제출대상자 발표일": "submission_candidate_announcement_date",
        "서류접수기간": "document_submission_deadline",
        "당첨자발표일": "winner_announcement_date",
        "계약기간": "contract_period"
    }
    
    for text in supply_schedule.text.split('\n'):
        for keyword in section_keywords.keys():
            if re.search(rf'{keyword}\s?:\s?([^~\n]*)', text):
                t = text.split(':')
                if t[0].strip() == '당첨자발표일' or t[0].strip() == '서류제출대상자 발표일':
                    p = False
                else:
                    p = True
                target_file['schedule'][section_keywords[t[0].strip()]] = cal_date(t[1].strip(), period=p)
            else:
                continue
    
    
    # 접수처 정보
    address = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sub_container"]/section[5]/div[1]/div/ul/li[1]')))
    target_file['reception_information']['address'] = address.text[6:] if len(address.text) > 6 else None
        
    phone_number = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sub_container"]/section[5]/div[1]/div/ul/li[2]')))
    if len(phone_number.text) > 7:
        target_file['reception_information']['phone_number'] = phone_number.text[7:]

    operating_period = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="sub_container"]/section[5]/div[1]/div/ul/li[3]')))
    target_file['reception_information']['operating_period'] = cal_date(operating_period.text, period=True)
    
    save_json(target_file, link_name)
    
    return target_file, link_name
    
