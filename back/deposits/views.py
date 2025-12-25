import requests
from django.conf import settings
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import (
    DepositProducts, DepositOptions, DepositSubscription,
    SavingProducts, SavingOptions, SavingSubscription
)
from .serializers import (
    DepositProductsSerializer, DepositOptionsSerializer, DepositSubscriptionSerializer,
    SavingProductsSerializer, SavingOptionsSerializer, SavingSubscriptionSerializer
)



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
@permission_classes([IsAuthenticated])
def save_deposit_products(request):
    """
    정기예금 상품 목록 및 옵션 목록 저장
    모든 금융권 데이터를 자동으로 저장
    (로그인 필요)
    """
    api_key = settings.API_KEY
    
    # 모든 금융권 코드
    fin_grp_list = ['020000', '030200', '030300', '050000', '060000']
    
    total_saved_products = 0
    total_saved_options = 0
    results_by_group = {}
    
    # 각 금융권별로 데이터 저장
    for top_fin_grp_no in fin_grp_list:
        params = {"auth": api_key, "topFinGrpNo": top_fin_grp_no, "pageNo": 1}
        
        try:
            # API 호출
            response = requests.get(API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if not data.get("result"):
                results_by_group[top_fin_grp_no] = {
                    "status": "error",
                    "message": "API 응답에 result가 없습니다."
                }
                continue

            result = data["result"]
            base_list = result.get("baseList", [])
            option_list = result.get("optionList", [])

            # 상품 기본 정보 저장
            saved_products = 0
            for product_data in base_list:
                product, created = DepositProducts.objects.update_or_create(
                    fin_prdt_cd=product_data.get("fin_prdt_cd"),
                    defaults={
                        "fin_co_no": product_data.get("fin_co_no", ""),
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
                    continue

            # 금융권별 결과 저장
            results_by_group[top_fin_grp_no] = {
                "status": "success",
                "saved_products": saved_products,
                "saved_options": saved_options,
                "total_products": len(base_list),
                "total_options": len(option_list),
            }
            
            total_saved_products += saved_products
            total_saved_options += saved_options

        except requests.exceptions.RequestException as e:
            results_by_group[top_fin_grp_no] = {
                "status": "error",
                "message": f"API 요청 실패: {str(e)}"
            }
        except Exception as e:
            results_by_group[top_fin_grp_no] = {
                "status": "error",
                "message": f"데이터 저장 실패: {str(e)}"
            }

    return Response(
        {
            "message": "모든 금융권 정기예금 상품 데이터 저장 완료",
            "total_saved_products": total_saved_products,
            "total_saved_options": total_saved_options,
            "results_by_group": results_by_group,
        },
        status=status.HTTP_201_CREATED,
    )

@api_view(["GET"])
@permission_classes([AllowAny])
def deposit_products(request):
    """
    전체 정기예금 상품 목록 출력 (비로그인 사용자 접근 가능)
    - 은행별 필터 기능 제공
    - 기간별 필터 (save_trm)
    - 금액별 필터 (min_amount)
    - 가입제한별 필터 (join_deny)
    - 1금융권 필터 (first_tier_only)
    - 옵션 정보 포함
    """
    products = DepositProducts.objects.all()
    
    # 은행별 필터링
    bank = request.GET.get('bank')
    if bank:
        products = products.filter(kor_co_nm__icontains=bank)
    
    # 기간별 필터링 (개월 수)
    save_trm = request.GET.get('save_trm')
    if save_trm:
        try:
            save_trm = int(save_trm)
            products = products.filter(options__save_trm=save_trm).distinct()
        except ValueError:
            pass
    
    # 금액별 필터링 (최소 금액)
    min_amount = request.GET.get('min_amount')
    if min_amount:
        try:
            min_amount = int(min_amount)
            products = products.filter(
                Q(max_limit__isnull=True) | Q(max_limit__gte=min_amount)
            )
        except ValueError:
            pass
    
    # 가입제한별 필터링 (join_deny)
    join_deny = request.GET.get('join_deny')
    if join_deny:
        try:
            join_deny = int(join_deny)
            products = products.filter(join_deny=join_deny)
        except ValueError:
            pass
    
    # 1금융권만 필터링 (신규 추가)
    first_tier_only = request.GET.get('first_tier_only')
    if first_tier_only and first_tier_only.lower() == 'true':
        # 1금융권 은행 목록
        first_tier_banks = [
            'KB국민은행', '신한은행', '하나은행', '우리은행', '농협은행', 'NH농협은행',
            '기업은행', 'IBK기업은행', '산업은행', 'KDB산업은행', '수협은행',
            '부산은행', 'BNK부산은행', '경남은행', 'BNK경남은행', '대구은행', 'DGB대구은행',
            '광주은행', '전북은행', 'JB전북은행', '제주은행',
            'SC제일은행', '한국씨티은행', '씨티은행', 'HSBC은행',
            '카카오뱅크', '케이뱅크', '토스뱅크'
        ]
        products = products.filter(kor_co_nm__in=first_tier_banks)
    
    serializer = DepositProductsSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
def deposit_product_detail(request, fin_prdt_cd):
    """
    특정 정기예금 상품의 상세 정보 출력 (비로그인 사용자 접근 가능)
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
def my_subscriptions_deposit(request):
    """
    로그인한 사용자가 가입한 모든 상품 조회
    """
    subscriptions = DepositSubscription.objects.filter(user=request.user)
    serializer = DepositSubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

SAVING_API_URL = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_saving_products(request):
    """
    적금 상품 목록 및 옵션 목록 저장
    모든 금융권 데이터를 자동으로 저장
    (로그인 필요)
    """
    api_key = settings.API_KEY
    
    # 모든 금융권 코드
    fin_grp_list = ['020000', '030200', '030300', '050000', '060000']
    
    total_saved_products = 0
    total_saved_options = 0
    results_by_group = {}
    
    # 각 금융권별로 데이터 저장
    for top_fin_grp_no in fin_grp_list:
        params = {"auth": api_key, "topFinGrpNo": top_fin_grp_no, "pageNo": 1}
        
        try:
            response = requests.get(SAVING_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if not data.get("result"):
                results_by_group[top_fin_grp_no] = {
                    "status": "error",
                    "message": "API 응답에 result가 없습니다."
                }
                continue

            result = data["result"]
            base_list = result.get("baseList", [])
            option_list = result.get("optionList", [])

            saved_products = 0
            for product_data in base_list:
                product, created = SavingProducts.objects.update_or_create(
                    fin_prdt_cd=product_data.get("fin_prdt_cd"),
                    defaults={
                        "fin_co_no": product_data.get("fin_co_no", ""),
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

            saved_options = 0
            for option_data in option_list:
                try:
                    fin_prdt_cd = option_data.get("fin_prdt_cd")
                    product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)

                    option, created = SavingOptions.objects.update_or_create(
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
                except SavingProducts.DoesNotExist:
                    continue
                except Exception:
                    continue

            results_by_group[top_fin_grp_no] = {
                "status": "success",
                "saved_products": saved_products,
                "saved_options": saved_options,
                "total_products": len(base_list),
                "total_options": len(option_list),
            }
            
            total_saved_products += saved_products
            total_saved_options += saved_options

        except requests.exceptions.RequestException as e:
            results_by_group[top_fin_grp_no] = {
                "status": "error",
                "message": f"API 요청 실패: {str(e)}"
            }
        except Exception as e:
            results_by_group[top_fin_grp_no] = {
                "status": "error",
                "message": f"데이터 저장 실패: {str(e)}"
            }

    return Response(
        {
            "message": "모든 금융권 적금 상품 데이터 저장 완료",
            "total_saved_products": total_saved_products,
            "total_saved_options": total_saved_options,
            "results_by_group": results_by_group,
        },
        status=status.HTTP_201_CREATED,
    )

@api_view(["GET"])
@permission_classes([AllowAny])
def saving_products(request):
    """
    전체 적금 상품 목록 출력 (비로그인 사용자 접근 가능)
    - 은행별 필터 기능 제공
    - 기간별 필터 (save_trm)
    - 금액별 필터 (min_amount)
    - 가입제한별 필터 (join_deny)
    - 1금융권 필터 (first_tier_only)
    """
    products = SavingProducts.objects.all()
    
    # 은행별 필터링
    bank = request.GET.get('bank')
    if bank:
        products = products.filter(kor_co_nm__icontains=bank)
    
    # 기간별 필터링 (개월 수)
    save_trm = request.GET.get('save_trm')
    if save_trm:
        try:
            save_trm = int(save_trm)
            products = products.filter(options__save_trm=save_trm).distinct()
        except ValueError:
            pass
    
    # 금액별 필터링 (최소 금액)
    min_amount = request.GET.get('min_amount')
    if min_amount:
        try:
            min_amount = int(min_amount)
            products = products.filter(
                Q(max_limit__isnull=True) | Q(max_limit__gte=min_amount)
            )
        except ValueError:
            pass
    
    # 가입제한별 필터링 (join_deny)
    join_deny = request.GET.get('join_deny')
    if join_deny:
        try:
            join_deny = int(join_deny)
            products = products.filter(join_deny=join_deny)
        except ValueError:
            pass
    
    # 1금융권만 필터링 (신규 추가)
    first_tier_only = request.GET.get('first_tier_only')
    if first_tier_only and first_tier_only.lower() == 'true':
        # 1금융권 은행 목록
        first_tier_banks = [
            'KB국민은행', '신한은행', '하나은행', '우리은행', '농협은행', 'NH농협은행',
            '기업은행', 'IBK기업은행', '산업은행', 'KDB산업은행', '수협은행',
            '부산은행', 'BNK부산은행', '경남은행', 'BNK경남은행', '대구은행', 'DGB대구은행',
            '광주은행', '전북은행', 'JB전북은행', '제주은행',
            'SC제일은행', '한국씨티은행', '씨티은행', 'HSBC은행',
            '카카오뱅크', '케이뱅크', '토스뱅크'
        ]
        products = products.filter(kor_co_nm__in=first_tier_banks)
    
    serializer = SavingProductsSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def saving_product_detail(request, fin_prdt_cd):
    """특정 적금 상품의 상세 정보 출력 (비로그인 사용자 접근 가능)"""
    try:
        product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        options = SavingOptions.objects.filter(product=product)
        
        product_serializer = SavingProductsSerializer(product)
        options_serializer = SavingOptionsSerializer(options, many=True)
        
        return Response({
            'product': product_serializer.data,
            'options': options_serializer.data
        }, status=status.HTTP_200_OK)
        
    except SavingProducts.DoesNotExist:
        return Response(
            {'error': '해당 상품을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def subscribe_saving(request, fin_prdt_cd):
    """적금 상품 가입"""
    try:
        product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        
        if SavingSubscription.objects.filter(user=request.user, product=product).exists():
            return Response(
                {'error': '이미 가입한 상품입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subscription = SavingSubscription.objects.create(
            user=request.user,
            product=product,
            selected_option_id=request.data.get('selected_option')
        )
        
        serializer = SavingSubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except SavingProducts.DoesNotExist:
        return Response(
            {'error': '상품을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def unsubscribe_saving(request, fin_prdt_cd):
    """적금 상품 가입 취소"""
    try:
        product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        subscription = SavingSubscription.objects.get(user=request.user, product=product)
        subscription.delete()
        
        return Response(
            {'message': '가입이 취소되었습니다.'},
            status=status.HTTP_200_OK
        )
        
    except (SavingProducts.DoesNotExist, SavingSubscription.DoesNotExist):
        return Response(
            {'error': '가입 정보를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_subscriptions_saving(request):
    """로그인한 사용자가 가입한 모든 적금 상품 조회"""
    subscriptions = SavingSubscription.objects.filter(user=request.user)
    serializer = SavingSubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)