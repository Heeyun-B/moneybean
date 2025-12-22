from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import os
from django.conf import settings
from datetime import datetime

def load_data(asset):
    """Excel 파일에서 데이터 로드"""
    base_dir = settings.BASE_DIR
    
    if asset == 'gold':
        file_path = os.path.join(base_dir, 'data', 'Gold_prices.xlsx')
    elif asset == 'silver':
        file_path = os.path.join(base_dir, 'data', 'Silver_prices.xlsx')
    else:
        return None
    
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

@api_view(['GET'])
def get_prices(request):
    """가격 데이터 API"""
    asset = request.GET.get('asset', 'gold')
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')
    
    # 1. asset 유효성 검증
    if asset not in ['gold', 'silver']:
        return Response({
            'error': '잘못된 자산 유형입니다. gold 또는 silver를 선택해주세요.'
        }, status=400)
    
    # 2. 날짜 형식 검증
    if start_date:
        try:
            start_dt = pd.to_datetime(start_date)
        except:
            return Response({
                'error': '시작 날짜 형식이 올바르지 않습니다. (예: 2023-01-01)'
            }, status=400)
    
    if end_date:
        try:
            end_dt = pd.to_datetime(end_date)
        except:
            return Response({
                'error': '종료 날짜 형식이 올바르지 않습니다. (예: 2023-12-31)'
            }, status=400)
    
    # 3. 시작일이 종료일보다 늦은 경우
    if start_date and end_date:
        if start_dt > end_dt:
            return Response({
                'error': '시작 날짜는 종료 날짜보다 이전이어야 합니다.'
            }, status=400)
    
    # 데이터 로드
    df = load_data(asset)
    
    if df is None:
        return Response({
            'error': '데이터를 불러올 수 없습니다.'
        }, status=500)
    
    # 날짜 컬럼 찾기
    date_column = None
    for col in df.columns:
        if col.lower() in ['date', 'dates', '날짜', 'datetime']:
            date_column = col
            break
    
    if date_column:
        # 날짜를 datetime 형식으로 변환
        df[date_column] = pd.to_datetime(df[date_column])
        
        # 4. 데이터 범위 확인
        data_min_date = df[date_column].min()
        data_max_date = df[date_column].max()
        
        # 날짜 필터링
        if start_date:
            df = df[df[date_column] >= start_dt]
        if end_date:
            df = df[df[date_column] <= end_dt]
        
        # 5. 필터링 후 데이터가 없는 경우
        if len(df) == 0:
            return Response({
                'error': f'선택한 기간에 데이터가 없습니다. 사용 가능한 데이터 범위: {data_min_date.strftime("%Y-%m-%d")} ~ {data_max_date.strftime("%Y-%m-%d")}',
                'available_range': {
                    'start': data_min_date.strftime('%Y-%m-%d'),
                    'end': data_max_date.strftime('%Y-%m-%d')
                }
            }, status=404)
        
        # 날짜를 문자열로 변환 (JSON 직렬화를 위해)
        df[date_column] = df[date_column].dt.strftime('%Y-%m-%d')
    
    # DataFrame을 딕셔너리 리스트로 변환
    data = df.to_dict('records')
    
    return Response({
        'asset': asset,
        'count': len(data),
        'data': data
    })