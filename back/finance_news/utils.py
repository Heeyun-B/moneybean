import requests
from datetime import datetime
from .models import NewsArticle
from django.conf import settings
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def extract_press_from_url(url):
    """
    URL에서 언론사 추출
    """
    try:
        match = re.search(r'/article/(\d+)/', url)
        if match:
            press_code = match.group(1)
            press_map = {
                '001': '연합뉴스', '002': 'JTBC', '003': '뉴시스',
                '005': '국민일보', '008': '머니투데이', '009': '매일경제',
                '011': '서울경제', '014': '파이낸셜뉴스', '015': '한국경제',
                '016': '헤럴드경제', '018': '이데일리', '020': '동아일보',
                '021': '문화일보', '022': '세계일보', '023': '조선일보',
                '025': '중앙일보', '028': '한겨레', '029': '디지털타임스',
                '030': '전자신문', '031': '아이뉴스24', '032': '경향신문',
                '081': '서울신문', '119': '데일리안', '138': '디지털데일리',
            }
            return press_map.get(press_code, f'언론사{press_code}')
        
        domain = urlparse(url).netloc
        return domain.replace('www.', '').split('.')[0]
        
    except:
        return ''


def crawl_article_content(url):
    """
    기사 본문 크롤링
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 네이버 뉴스 본문 선택자들
        content_selectors = [
            '#dic_area',           # 네이버 뉴스 기본
            '#articeBody',         # 일부 네이버 뉴스
            '.news_end',           # 네이버 뉴스
            'article',             # 일반 article 태그
            '.article_body',       # 일부 언론사
            '.article-body',       # 일부 언론사
            '#articleBodyContents' # 일부 언론사
        ]
        
        content = ''
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # 불필요한 태그 제거
                for tag in content_elem.find_all(['script', 'style', 'iframe', 'ins']):
                    tag.decompose()
                
                content = content_elem.get_text(strip=True)
                
                # 너무 짧으면 다음 선택자 시도
                if len(content) > 100:
                    break
        
        return content[:5000] if content else ''  # 최대 5000자
        
    except Exception as e:
        print(f"본문 크롤링 실패 ({url}): {e}")
        return ''


def crawl_naver_news_api(query="금융"):
    """
    네이버 검색 API로 뉴스 크롤링
    """
    client_id = settings.NAVER_CLIENT_ID
    client_secret = settings.NAVER_CLIENT_SECRET
    
    url = "https://openapi.naver.com/v1/search/news.json"
    
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    
    params = {
        "query": query,
        "display": 10,
        "sort": "date"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        crawled_count = 0
        
        for item in data.get('items', []):
            try:
                # HTML 태그 제거
                title = item['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
                description = item['description'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
                link = item['link']
                original_link = item.get('originallink', link)
                
                # 중복 체크
                if NewsArticle.objects.filter(link=link).exists():
                    print(f"중복 스킵: {title}")
                    continue
                
                # 언론사 추출
                press = extract_press_from_url(link)
                if not press:
                    press = extract_press_from_url(original_link)
                
                # 날짜 파싱
                pub_date_str = item['pubDate']
                pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z')
                
                # 기사 본문 크롤링
                print(f"본문 크롤링 중: {title}")
                content = crawl_article_content(link)
                
                # 본문이 없으면 description 사용
                if not content:
                    content = description
                    print(f"  -> 본문 크롤링 실패, description 사용")
                else:
                    print(f"  -> 본문 크롤링 성공 ({len(content)}자)")
                
                # DB에 저장
                NewsArticle.objects.create(
                    title=title,
                    content=content,
                    link=link,
                    press=press,
                    published_date=pub_date,
                )
                
                crawled_count += 1
                print(f"✓ 저장 완료: {title} - {press}")
                
            except Exception as e:
                print(f"Error saving article: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        return {
            'success': True,
            'crawled_count': crawled_count,
            'message': f'{crawled_count}개의 기사를 크롤링했습니다.'
        }
        
    except Exception as e:
        print(f"API Error: {e}")
        return {
            'success': False,
            'message': f'크롤링 실패: {str(e)}'
        }