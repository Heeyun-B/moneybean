import openai
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from django.conf import settings
from .models import NewsArticle
from .serializers import NewsArticleSerializer, NewsArticleListSerializer
from .utils import crawl_naver_news_api

# GPT 클라이언트 설정
client = openai.OpenAI(
    api_key=settings.GMS_API_KEY,
    base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1"
)

@api_view(['GET'])
@permission_classes([AllowAny])
def news_list(request):
    """뉴스 목록 조회"""
    articles = NewsArticle.objects.all()
    serializer = NewsArticleListSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def news_detail(request, news_pk):
    """뉴스 상세 조회 및 content 필드에 요약 데이터 반환"""
    try:
        # 1. 기사 조회
        article = NewsArticle.objects.get(pk=news_pk)
    except NewsArticle.DoesNotExist:
        return Response({'error': '기사를 찾을 수 없습니다.'}, 
                        status=status.HTTP_404_NOT_FOUND)

    # 2. 기본 데이터 직렬화 (JSON 변환)
    serializer = NewsArticleSerializer(article)
    data = serializer.data  # 시리얼라이저 결과 데이터를 변수에 할당

    # 3. 요약 조건 확인 (본문이 충분히 긴 경우에만 실행)
    if article.content and len(article.content) >= 100:
        try:
            # GPT API 호출용 프롬프트 작성
            prompt_content = f"""
            다음 금융 기사를 쉽고 명확하게 요약해주세요.
            제목: {article.title}
            본문: {article.content}
            
            형식:
            # 📰 기사 요약
            ## 🔑 핵심 내용
            (3줄 요약)
            """

            # OpenAI API 호출
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "당신은 금융 기사를 요약하는 전문 AI입니다."},
                    {"role": "user", "content": prompt_content}
                ],
                temperature=0.3
            )
            
            # 4. 중요: 기존 content 내용을 AI 요약본으로 교체
            data['content'] = response.choices[0].message.content

        except Exception as e:
            # API 오류 발생 시 원본 content를 유지하거나 에러 메시지 추가
            data['content'] = f"요약 생성 중 오류가 발생했습니다. 원본 내용: {article.content[:100]}..."
    
    # 5. 최종 데이터 반환
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def crawl_news(request):
    """뉴스 크롤링 실행"""
    from .utils import crawl_naver_news_api
    
    query = request.data.get('query', '금융')
    result = crawl_naver_news_api(query)
    
    if result['success']:
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)