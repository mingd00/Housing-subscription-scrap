## JSON 파일 형식

```json
{
    "agencyType": 기관(LH, IH 등),
    "house_types": 유형(행복 주택, 공공 임대 등),
    "default_residence_period": 기본 거주 기간,
    "schedule": {
        "announcement_date": "2025-01-13"(모집 공고일),
        "general_supply_date": ["2025-01-23", "2025-01-23"](일반 공급 날짜),
        "winner_announcement_date": "2025-03-31"(당첨자 발표일),
        "document_submission_deadline": ["2025-01-23", "2025-01-23"](서류 접수 기간),
        "submission_candidate_announcement_date": "2025-03-31"(서류 제출 대상자 발표일)
    },
    "complex_info": [
        {
            "complex_name": "단지 이름1",
            "units": [
                {
                    "type": "타입1",
                    "eligible_residents": ["대상1", "대상2"],
                    "current_supply": 현재 공급 세대 수,
                    "exclusive_area_m2": 전용 면적,
                    "heating": 난방,
                    "images": 평면도
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

    "housing_supply"(임대 가격): [
        {
            "block": "단지 이름1",
            "types": [
                {
                    "type": "타입 1",
                    "target": [
                        {
                            "group": "대학생, 청년(소득×)"(타입),
                            "contract": {
                                "total_deposit": 임대 보증금 합계,
                                "down_payment": 임대 보증금 계약금,
                                "balance": 임대 보증금 잔금,
                                "monthly_rent": 월 임대료
                            },
                            "converted"(전환): {
                                "limit"(전환 가능 보증금 한도액): {
                                    "plus": "-",
                                    "minus": 8000000,
                                },
                                "LeaseTerm_MaximumConversion"(최대 전환시 임대 조건): {
                                    "balance": 임대 보증금,
                                    "monthly_rent": 월 임대료
                                }
                            }
                        },
                        {
                            "group": "청년(소득○)",
                            ...생략...
                        },
                    ]
                },
                {
                    "type": "타입 2",
                    ...생략...
                }
            ],
            "block": "단지 이름2",
            ...생략...
        }
    ],

    "reception_information"(접수처 정보): {
        "address": 소재지,
        "phone_number": 전화번호,
        "operating_period": 운영 기간
    }
}
```
