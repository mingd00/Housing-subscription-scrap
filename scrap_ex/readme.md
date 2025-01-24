## JSON 파일 형식

```json
{
    "agencyType": 기관(LH, IH 등),
    "house_type": 유형(행복 주택, 공공 임대 등),
    "default_residence_period": 기본 거주 기간,
    "schedule": {
        "announcement_date": "2025-01-13"(모집 공고일),
        "application_period": ["2025-01-23", "2025-01-23"](접수 기간),
        "winner_announcement_date": "2025-01-23"(당첨자 발표일),
        "contract_period": ["2025-01-23", "2025-01-23"](계약 기간),
        "document_submission_deadline": ["2025-01-23", "2025-01-23"](서류 접수 기간),
        "submission_candidate_announcement_date": "2025-03-31"(서류 제출 대상자 발표일)
    },
    "reception_information"(접수처 정보): {
        "address": 소재지,
        "phone_number": 전화번호,
        "operating_period": 운영 기간
    }
    "complex_info": [
        {
            "complex_name": "단지 이름1",
            "location": "단지 주소",
            "heating": "난방",
            "units": [
                {
                    "type": "타입1",
                    "eligible_residents": ["대상1", "대상2"],
                    "current_supply": 현재 공급 세대 수,
                    "exclusive_area_m2": 전용 면적,
                    "images": 평면도,
                    "target": [
                        {
                            "group": "대학생",
                            "contract": {
                                "down_payment": 계약금,
                                "deposit_max": 최대 보증금,
                                "deposit_min": 최소 보증금,
                                "monthly_rent_min": 최소 월세,
                                "monthly_rent_max": 최대 월세
                            }
                        },
                        {
                            "group": "청년(무소득)"
                            ...생략...
                        },
                        ...생략...
                    ]
                },
                {
                    "type": "타입2",
                    ...생략...

                },
                ...생략...
            ],
            "house_images"(평면도 외 사진들): {
                {
                    "location_map": 위치도,
                    "complex_overview": 단지 조감도,
                    "complex_site_plan": 단지 배치도,
                    "unit_layout_plan": 동호 배치도
                }

            }
        },
        {
            "complex_name": "단지 이름2",
            ...생략...
        },
    ],
}
```
