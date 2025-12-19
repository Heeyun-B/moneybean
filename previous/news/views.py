from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
from .models import News
import json

# Create your views here.
def index(request):
    return render(request, "news/index.html")

@csrf_exempt
def fetch_news(request):
    if request.method == 'POST':
        try:
            # 프론트엔드에서 보낸 검색어 받기
            data = json.loads(request.body)
            query = data.get('query', '')
            
            if not query:
                return JsonResponse({'error': '검색어를 입력해주세요.'}, status=400)
            
            # NAVER 뉴스 API 호출
            url = 'https://openapi.naver.com/v1/search/news.json'
            headers = {
                'X-Naver-Client-Id': settings.NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': settings.NAVER_CLIENT_SECRET,
            }
            params = {
                'query': query,
                'display': 100,  # 최대 100개
                'sort': 'date'   # 최신순 정렬
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                news_data = response.json()
                items = news_data.get('items', [])
                
                saved_count = 0
                duplicated_count = 0
                
                for item in items:
                    title = item.get('title', '').replace('<b>', '').replace('</b>', '')
                    link = item.get('link', '')
                    description = item.get('description', '').replace('<b>', '').replace('</b>', '')
                    
                    # 중복 체크 및 저장
                    if not News.objects.filter(title=title).exists():
                        News.objects.create(
                            title=title,
                            link=link,
                            description=description
                        )
                        saved_count += 1
                    else:
                        duplicated_count += 1
                
                return JsonResponse({
                    'success': True,
                    'message': f'총 {saved_count}개의 뉴스가 저장되었습니다. (중복 {duplicated_count}개)',
                    'saved': saved_count,
                    'duplicated': duplicated_count
                })
            else:
                return JsonResponse({'error': 'NAVER API 호출 실패'}, status=500)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

def view_all_news(request):
    news_list = News.objects.all().order_by('-created_at')
    news_data = [{
        'id': news.id,
        'title': news.title,
        'link': news.link,
        'description': news.description,
        'is_bookmarked': news.is_bookmarked,
        'created_at': news.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for news in news_list]
    
    return JsonResponse({'news': news_data})

def view_bookmarked_news(request):
    """북마크된 뉴스만 조회"""
    news_list = News.objects.filter(is_bookmarked=True).order_by('-created_at')
    news_data = [{
        'id': news.id,
        'title': news.title,
        'link': news.link,
        'description': news.description,
        'is_bookmarked': news.is_bookmarked,
        'created_at': news.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for news in news_list]
    
    return JsonResponse({'news': news_data})

def news_detail(request, news_id):
    try:
        news = News.objects.get(id=news_id)
        return JsonResponse({
            'success': True,
            'news': {
                'id': news.id,
                'title': news.title,
                'description': news.description,
                'link': news.link,
                'is_bookmarked': news.is_bookmarked,
                'created_at': news.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    except News.DoesNotExist:
        return JsonResponse({'error': '뉴스를 찾을 수 없습니다.'}, status=404)
    
@csrf_exempt
def toggle_bookmark(request, news_id):
    if request.method == 'POST':
        try:
            news = News.objects.get(id=news_id)
            news.is_bookmarked = not news.is_bookmarked
            news.save()
            
            return JsonResponse({
                'success': True,
                'is_bookmarked': news.is_bookmarked,
                'message': '북마크에 추가되었습니다.' if news.is_bookmarked else '북마크가 해제되었습니다.'
            })
        except News.DoesNotExist:
            return JsonResponse({'error': '뉴스를 찾을 수 없습니다.'}, status=404)
    
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)