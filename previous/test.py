# test_api.py (임시 테스트 파일)
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'

params = {
    'auth': API_KEY,
    'topFinGrpNo': '020000',  # 은행
    'pageNo': 1
}

response = requests.get(BASE_URL, params=params)
data = response.json()

# 응답 구조 확인
print(json.dumps(data, indent=2, ensure_ascii=False))

# 상품 리스트와 옵션 리스트 구조 확인
if 'result' in data:
    print("\n=== 상품 기본 정보 ===")
    if data['result'].get('baseList'):
        print(json.dumps(data['result']['baseList'][0], indent=2, ensure_ascii=False))
    
    print("\n=== 상품 옵션 정보 ===")
    if data['result'].get('optionList'):
        print(json.dumps(data['result']['optionList'][0], indent=2, ensure_ascii=False))