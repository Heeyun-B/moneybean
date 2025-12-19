import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DepositProducts, DepositOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer

API_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'

def safe_int(value, default=0):
    """안전하게 int로 변환"""
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=-1):
    """안전하게 float로 변환"""
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

@api_view(['GET'])
def save_deposit_products(request):
    """
    정기예금 상품 목록 및 옵션 목록 저장
    """
    api_key = settings.API_KEY
    
    params = {
        'auth': api_key,
        'topFinGrpNo': '020000',  # 은행
        'pageNo': 1
    }
    
    try:
        # API 호출
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('result'):
            return Response({
                'error': 'API 응답에 result가 없습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        result = data['result']
        base_list = result.get('baseList', [])
        option_list = result.get('optionList', [])
        
        # 상품 기본 정보 저장
        saved_products = 0
        for product_data in base_list:
            product, created = DepositProducts.objects.update_or_create(
                fin_prdt_cd=product_data.get('fin_prdt_cd'),
                defaults={
                    'kor_co_nm': product_data.get('kor_co_nm', ''),
                    'fin_prdt_nm': product_data.get('fin_prdt_nm', ''),
                    'etc_note': product_data.get('etc_note', ''),
                    'join_deny': safe_int(product_data.get('join_deny'), 1),
                    'join_member': product_data.get('join_member', ''),
                    'join_way': product_data.get('join_way', ''),
                    'spcl_cnd': product_data.get('spcl_cnd', ''),
                    'mtrt_int': product_data.get('mtrt_int', ''),
                    'max_limit': product_data.get('max_limit'),
                    'dcls_month': product_data.get('dcls_month', ''),
                    'dcls_strt_day': product_data.get('dcls_strt_day', ''),
                    'dcls_end_day': product_data.get('dcls_end_day'),
                    'fin_co_subm_day': product_data.get('fin_co_subm_day', ''),
                }
            )
            if created:
                saved_products += 1
        
        # 옵션 정보 저장
        saved_options = 0
        for option_data in option_list:
            try:
                fin_prdt_cd = option_data.get('fin_prdt_cd')
                product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
                
                option, created = DepositOptions.objects.update_or_create(
                    product=product,
                    intr_rate_type=option_data.get('intr_rate_type', ''),
                    save_trm=safe_int(option_data.get('save_trm')),
                    defaults={
                        'intr_rate_type_nm': option_data.get('intr_rate_type_nm', ''),
                        'intr_rate': safe_float(option_data.get('intr_rate')),
                        'intr_rate2': safe_float(option_data.get('intr_rate2')),
                    }
                )
                if created:
                    saved_options += 1
            except DepositProducts.DoesNotExist:
                continue
            except Exception:
                # 개별 옵션 저장 실패해도 계속 진행
                continue
        
        return Response({
            'message': '정기예금 상품 목록 데이터 저장 성공',
            'saved_products': saved_products,
            'saved_options': saved_options,
            'total_products': len(base_list),
            'total_options': len(option_list)
        }, status=status.HTTP_201_CREATED)
        
    except requests.exceptions.RequestException as e:
        return Response({
            'error': f'API 요청 실패: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({
            'error': f'데이터 저장 실패: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def deposit_products(request):
    """
    전체 정기예금 상품 목록 출력
    """
    products = DepositProducts.objects.all()
    serializer = DepositProductsSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)