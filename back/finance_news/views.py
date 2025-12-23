from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import NewsArticle
from .serializers import NewsArticleSerializer, NewsArticleListSerializer
from .utils import crawl_naver_news_api

@api_view(['GET'])
def news_list(request):
    """뉴스 목록 조회"""
    articles = NewsArticle.objects.all()
    serializer = NewsArticleListSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def news_detail(request, news_pk):
    """뉴스 상세 조회"""
    try:
        article = NewsArticle.objects.get(pk=news_pk)
    except NewsArticle.DoesNotExist:
        return Response({'error': '기사를 찾을 수 없습니다.'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    serializer = NewsArticleSerializer(article)
    return Response(serializer.data)

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