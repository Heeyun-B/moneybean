from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import os
from django.conf import settings
from .utils import clean_and_interpolate_prices

def load_data(asset):
    base_dir = settings.BASE_DIR
    file_path = os.path.join(base_dir, 'data', 'Gold_prices.xlsx' if asset == 'gold' else 'Silver_prices.xlsx')
    
    try:
        df = pd.read_excel(file_path)
        
        # 1. 컬럼 찾기
        date_col = next((c for c in df.columns if c.lower() in ['date', 'dates', '날짜']), None)
        price_col = next((c for c in df.columns if c.lower() in ['price', 'close', '종가', 'close/last']), None)
        
        if date_col and price_col:
            # 날짜 형식 변환
            df[date_col] = pd.to_datetime(df[date_col])
            
            # 가격 데이터가 문자열(1,234.56)인 경우 숫자로 변환
            if df[price_col].dtype == 'object':
                df[price_col] = df[price_col].astype(str).str.replace(',', '').str.replace('$', '')
            df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
            
            # 데이터 정제 및 환율 계산 호출
            df = clean_and_interpolate_prices(df, price_col, date_col)
            
        return df
    except Exception as e:
        print(f"데이터 로드 중 에러 발생: {e}")
        return None

@api_view(['GET'])
def get_prices(request):
    asset = request.GET.get('asset', 'gold')
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')
    
    # 기본 검증
    if asset not in ['gold', 'silver']:
        return Response({'error': '잘못된 자산 유형입니다.'}, status=400)
    
    df = load_data(asset)
    if df is None:
        return Response({'error': '데이터를 처리하는 중 서버 에러가 발생했습니다.'}, status=500)
    
    date_column = next((c for c in df.columns if c.lower() in ['date', 'dates', '날짜', 'datetime']), None)
    
    if date_column:
        df[date_column] = pd.to_datetime(df[date_column])
        
        # 날짜 필터링
        if start_date:
            df = df[df[date_column] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df[date_column] <= pd.to_datetime(end_date)]
        
        if len(df) == 0:
            return Response({'error': '해당 기간에 데이터가 없습니다.'}, status=404)
        
        df[date_column] = df[date_column].dt.strftime('%Y-%m-%d')
    
    data = df.to_dict('records')
    return Response({'asset': asset, 'count': len(data), 'data': data})