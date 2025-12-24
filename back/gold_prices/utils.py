import pandas as pd
import numpy as np
import yfinance as yf

def clean_and_interpolate_prices(df, price_column, date_column):
    """
    1. 가격 데이터 정제 (문자열 -> NaN -> 보간)
    2. 해당 기간의 실제 과거 환율(yfinance)을 가져와 병합
    3. 일자별 실제 환율을 적용하여 원화 환산
    """
    # [1] 가격 데이터 정제
    df[price_column] = pd.to_numeric(df[price_column], errors='coerce')
    df[price_column] = df[price_column].interpolate(method='linear', limit_direction='both')

    # [2] 환율 데이터 가져오기 (2023-2024)
    start_date = df[date_column].min()
    end_date = df[date_column].max()
    
    # yfinance로 원/달러 환율(USDKRW=X) 로드
    ex_df = yf.download("USDKRW=X", start=start_date, end=end_date)
    
    if not ex_df.empty:
        # 환율 데이터의 인덱스를 컬럼으로 빼고 날짜 형식 통일
        ex_df = ex_df[['Close']].reset_index()
        ex_df.columns = [date_column, 'Exchange_Rate']
        
        # [3] 금/은 데이터와 환율 데이터 병합 (날짜 기준 Left Join)
        df = pd.merge(df, ex_df, on=date_column, how='left')
        
        # 주말 등 환율 데이터가 없는 날은 앞의 환율로 채움 (Forward Fill)
        df['Exchange_Rate'] = df['Exchange_Rate'].ffill().bfill()
        
        # [4] 원화 환산 (1g당 가격)
        OZ_TO_G = 31.1034768
        df['price_krw_g'] = (df[price_column] / OZ_TO_G) * df['Exchange_Rate']
        df['price_krw_g'] = df['price_krw_g'].round(2)
        
    return df