import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import DepositProducts, DepositOptions, DepositSubscription
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, DepositSubscriptionSerializer



API_URL = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"


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


@api_view(["POST"])
def save_deposit_products(request):
    """
    정기예금 상품 목록 및 옵션 목록 저장
    """
    api_key = settings.API_KEY

    params = {"auth": api_key, "topFinGrpNo": "020000", "pageNo": 1}  # 은행

    try:
        # API 호출
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("result"):
            return Response(
                {"error": "API 응답에 result가 없습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = data["result"]
        base_list = result.get("baseList", [])
        option_list = result.get("optionList", [])

        # 상품 기본 정보 저장
        saved_products = 0
        for product_data in base_list:
            product, created = DepositProducts.objects.update_or_create(
                fin_prdt_cd=product_data.get("fin_prdt_cd"),
                defaults={
                    "kor_co_nm": product_data.get("kor_co_nm", ""),
                    "fin_prdt_nm": product_data.get("fin_prdt_nm", ""),
                    "etc_note": product_data.get("etc_note", ""),
                    "join_deny": safe_int(product_data.get("join_deny"), 1),
                    "join_member": product_data.get("join_member", ""),
                    "join_way": product_data.get("join_way", ""),
                    "spcl_cnd": product_data.get("spcl_cnd", ""),
                    "mtrt_int": product_data.get("mtrt_int", ""),
                    "max_limit": product_data.get("max_limit"),
                    "dcls_month": product_data.get("dcls_month", ""),
                    "dcls_strt_day": product_data.get("dcls_strt_day", ""),
                    "dcls_end_day": product_data.get("dcls_end_day"),
                    "fin_co_subm_day": product_data.get("fin_co_subm_day", ""),
                },
            )
            if created:
                saved_products += 1

        # 옵션 정보 저장
        saved_options = 0
        for option_data in option_list:
            try:
                fin_prdt_cd = option_data.get("fin_prdt_cd")
                product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)

                option, created = DepositOptions.objects.update_or_create(
                    product=product,
                    intr_rate_type=option_data.get("intr_rate_type", ""),
                    save_trm=safe_int(option_data.get("save_trm")),
                    defaults={
                        "intr_rate_type_nm": option_data.get("intr_rate_type_nm", ""),
                        "intr_rate": safe_float(option_data.get("intr_rate")),
                        "intr_rate2": safe_float(option_data.get("intr_rate2")),
                    },
                )
                if created:
                    saved_options += 1
            except DepositProducts.DoesNotExist:
                continue
            except Exception:
                # 개별 옵션 저장 실패해도 계속 진행
                continue

        return Response(
            {
                "message": "정기예금 상품 목록 데이터 저장 성공",
                "saved_products": saved_products,
                "saved_options": saved_options,
                "total_products": len(base_list),
                "total_options": len(option_list),
            },
            status=status.HTTP_201_CREATED,
        )

    except requests.exceptions.RequestException as e:
        return Response(
            {"error": f"API 요청 실패: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except Exception as e:
        return Response(
            {"error": f"데이터 저장 실패: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def deposit_products(request):
    """
    전체 정기예금 상품 목록 출력
    - 은행별 필터 기능 제공
    - 옵션 정보 포함
    """
    products = DepositProducts.objects.all()
    
    # 은행별 필터링
    bank = request.GET.get('bank')  # ?bank=우리은행
    if bank:
        products = products.filter(kor_co_nm__icontains=bank)
    
    serializer = DepositProductsSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def deposit_product_detail(request, fin_prdt_cd):
    """
    특정 정기예금 상품의 상세 정보 출력
    상품 기본 정보 + 해당 상품의 모든 옵션 정보 반환
    """
    try:
        # 상품 조회
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        
        # 해당 상품의 옵션들 조회
        options = DepositOptions.objects.filter(product=product)
        
        # 직렬화
        product_serializer = DepositProductsSerializer(product)
        options_serializer = DepositOptionsSerializer(options, many=True)
        
        return Response({
            'product': product_serializer.data,
            'options': options_serializer.data
        }, status=status.HTTP_200_OK)
        
    except DepositProducts.DoesNotExist:
        return Response(
            {'error': '해당 상품을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def subscribe_product(request, fin_prdt_cd):
    """
    특정 정기예금 상품에 가입
    """
    try:
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        
        # 이미 가입했는지 확인
        if DepositSubscription.objects.filter(user=request.user, product=product).exists():
            return Response(
                {'error': '이미 가입한 상품입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 가입 처리
        subscription = DepositSubscription.objects.create(
            user=request.user,
            product=product,
            selected_option_id=request.data.get('selected_option')
        )
        
        serializer = DepositSubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except DepositProducts.DoesNotExist:
        return Response(
            {'error': '상품을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def unsubscribe_product(request, fin_prdt_cd):
    """
    특정 정기예금 상품 가입 취소
    """
    try:
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        subscription = DepositSubscription.objects.get(user=request.user, product=product)
        subscription.delete()
        
        return Response(
            {'message': '가입이 취소되었습니다.'},
            status=status.HTTP_200_OK
        )
        
    except (DepositProducts.DoesNotExist, DepositSubscription.DoesNotExist):
        return Response(
            {'error': '가입 정보를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_subscriptions(request):
    """
    로그인한 사용자가 가입한 모든 상품 조회
    """
    subscriptions = DepositSubscription.objects.filter(user=request.user)
    serializer = DepositSubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)