import json
import os

# 'json' 폴더 내의 모든 파일을 순회
folder_path = 'json'
for filename in os.listdir(folder_path):
    # 확장자가 .json인 파일만 처리
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        # JSON 파일 열기
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 복잡한 구조의 데이터 처리
        for complex_info in data.get('complex_info', []):
            for unit in complex_info.get('units', []):
                all_eligible_residents = []
                
                for target in unit.get('target', []):
                    group = target.get('group')
                    
                    # group이 None이면 빈 문자열로 변환
                    if group is not None:
                        group = group.strip().replace('·', ',')
                        
                        if any(keyword in group for keyword in ['소득X 청년', '청년(소득×)', '청년(소득無)']):
                            group = '청년(소득X)'
                        elif any(keyword in group for keyword in ['청년(소득有)', '청년(소득○)', '소득O 청년']):
                            group = '청년(소득O)'
                        
                        # 다시 한 번 쉼표 변환 보장
                        group = group.replace('·', ',')
                        
                        # 쉼표로 구분된 값 추가 (공백 제거)
                        all_eligible_residents.extend([g.strip() for g in group.split(',')])
                        
                        # 변환된 group 값을 다시 target['group']에 반영
                        target['group'] = group
                
                # eligible_residents 설정 (값이 없으면 None 할당)
                unit['eligible_residents'] = list(set(all_eligible_residents)) if all_eligible_residents else None
        
        # 처리된 데이터를 같은 파일명으로 덮어쓰기
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"Updated {filename}")
