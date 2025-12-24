import openai
import re
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings

# 1. GMS 클라이언트
client = openai.OpenAI(
    api_key=settings.GMS_API_KEY,
    base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1" 
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def diagnosis(request):
    """
    GPT-4o를 사용하여 자산 진단 리포트 생성
    """
    try:
        # Vue에서 보낸 데이터 추출
        data = request.data
        total_assets = data.get('totalAssets', 0)
        total_cash = data.get('totalCash', 0)
        total_invest = data.get('totalInvest', 0)
        total_debt = data.get('totalDebt', 0)
        net_worth = data.get('netWorth', 0)
        income = data.get('income', 0)
        expense = data.get('expense', 0)
        sections = data.get('sections', [])

        # 비율 계산
        cash_ratio = (total_cash / total_assets * 100) if total_assets > 0 else 0
        invest_ratio = (total_invest / total_assets * 100) if total_assets > 0 else 0

        # GPT 전달용 프롬프트 조립
        prompt_content = f"""
당신은 20년 경력의 전문 금융 컨설턴트입니다. 다음 고객의 자산 포트폴리오를 분석하고 실용적인 조언을 제공해주세요.

## 📊 고객 자산 현황
- **월 소득/지출**: {income:,.0f}원 / {expense:,.0f}원
- **총 자산**: {total_assets:,.0f}원 (현금 {cash_ratio:.1f}%, 투자 {invest_ratio:.1f}%)
- **부채/순자산**: {total_debt:,.0f}원 / {net_worth:,.0f}원

### 상세 자산 내역
"""
        for sec in sections:
            prompt_content += f"\n[{sec['label']}] (합계: {sec['total']:,.0f}원)\n"
            for group in sec.get('groups', []):
                prompt_content += f"- {group['categoryName']}: {group['totalValue']:,.0f}원\n"
                for item in group.get('items', []):
                    prompt_content += f"  └ {item['name']}: {float(item.get('current_value', 0)):,.0f}원\n"

        prompt_content += """
## 📋 분석 요청사항
다음 형식으로 **한국어**로 상세하게 분석해주세요:
# 💰 자산 진단 리포트

## 📊 포트폴리오 분석
(이 섹션 안에 다음 내용을 포함하여 하나의 글로 작성해주세요)
1. 자산 구성: 총 자산 대비 현금 및 투자 자산의 비율과 그에 대한 진단
2. 부채 상황: 총 부채와 순자산 현황 및 부채 관리 전략

## 💪 강점
## ⚠️ 개선이 필요한 부분
## 💡 맞춤 실행 제안
## 📈 기대 효과

**작성 가이드:**
- **중요**: '자산 구성'이나 '부채 상황'을 별도의 '## 제목'으로 만들지 마세요.
- 오직 '## 📊 포트폴리오 분석'이라는 제목 아래에 모든 내용을 서술형으로 작성하세요.
- 친근하고 공감하는 톤으로 작성
- 구체적인 숫자와 비율 언급
- 전문 용어는 쉽게 풀어서 설명
- 가독성이 좋게 이모티콘 활용
"""

        # GPT API 호출
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "당신은 고객의 자산을 분석하여 최적의 금융 솔루션을 제공하는 AI 비서 '머니빈'입니다."},
                {"role": "user", "content": prompt_content}
            ],
            temperature=0.7
        )

        full_report = response.choices[0].message.content
        
        # 섹션별로 파싱
        parsed_sections = parse_report_sections(full_report)
        
        # 결과 반환 (sections만)
        return Response({
            'success': True,
            'sections': parsed_sections
        })

    except Exception as e:
        return Response({
            'success': False,
            'error': f'GPT 진단 중 오류가 발생했습니다: {str(e)}'
        }, status=500)


def parse_report_sections(report_text):
    """
    리포트를 섹션별로 파싱 (# 제목과 ## 제목 모두 포함)
    """
    sections = []
    
    # # 제목 찾기 (자산 진단 리포트)
    main_title_pattern = r'^#\s+(.+?)$'
    main_title_match = re.search(main_title_pattern, report_text, re.MULTILINE)
    
    # # 제목 이후부터 첫 번째 ## 제목 전까지의 내용 (있다면)
    main_content = ''
    if main_title_match:
        main_title_end = main_title_match.end()
        first_section_match = re.search(r'##', report_text[main_title_end:])
        if first_section_match:
            main_content = report_text[main_title_end:main_title_end + first_section_match.start()].strip()
        else:
            main_content = report_text[main_title_end:].strip()
        
        sections.append({
            'title': main_title_match.group(1).strip(),
            'content': main_content,
            'is_main': True
        })
    
    # ## 으로 시작하는 하위 제목들
    pattern = r'##\s+(.+?)(?=##|$)'
    matches = re.finditer(pattern, report_text, re.DOTALL)
    
    for match in matches:
        full_text = match.group(0).strip()
        
        # 제목과 내용 분리
        lines = full_text.split('\n', 1)
        title = lines[0].replace('##', '').strip()
        content = lines[1].strip() if len(lines) > 1 else ''
        
        sections.append({
            'title': title,
            'content': content,
            'is_main': False
        })
    
    return sections
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def luck(request):
    """
    오늘의 금융 운세 생성 (생년월일 기반)
    """
    try:
        user = request.user
        
        # 생년월일이 없으면 에러 반환
        if not user.birth_date:
            return Response({
                'success': False,
                'error': 'birth_date_required',
                'message': '생년월일 정보가 필요합니다. 프로필 설정에서 생년월일을 입력해주세요.'
            }, status=400)
        
        # 생년월일 정보 준비
        from datetime import datetime
        today = datetime.now()
        age = today.year - user.birth_date.year
        birth_year = user.birth_date.year
        birth_month = user.birth_date.month
        birth_day = user.birth_date.day
        
        birth_info = f"""
- 생년월일: {birth_year}년 {birth_month}월 {birth_day}일
- 나이: 만 {age}세
"""
        
        # 프롬프트 작성
        prompt_content = f"""
당신은 재미있고 긍정적인 금융 운세를 제공하는 AI입니다.
다음 정보를 바탕으로 오늘의 금융 운세를 작성해주세요.

## 사용자 정보
{birth_info}

다음 형식으로 작성해주세요:

# 🍀 오늘의 금융 운세

## 💰 오늘의 재물운
(생년월일을 고려한 오늘의 재물운 메시지)

## 💳 추천 금융 활동
(나이대에 맞는 금융 활동 1-2가지 추천)

## 🎯 럭키 넘버 
(생년월일과 관련된 행운의 숫자와 그 의미)

## 💡 한 줄 조언
(오늘 하루를 위한 짧고 임팩트 있는 조언)

**작성 가이드:**
- 생년월일 정보를 자연스럽게 활용
- 나이대에 맞는 실질적인 금융 조언 제공
- 밝고 긍정적인 톤
- 재미있지만 진지한 조언
- 200-300자 분량
"""

        # GPT API 호출
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 재미있고 유익한 금융 운세를 제공하는 AI입니다. 생년월일 정보를 자연스럽게 활용하여 개인화된 운세를 제공하세요."},
                {"role": "user", "content": prompt_content}
            ],
            temperature=0.9
        )

        return Response({
            'success': True,
            'luck_message': response.choices[0].message.content
        })

    except Exception as e:
        return Response({
            'success': False,
            'error': 'api_error',
            'message': f'운세 생성 중 오류가 발생했습니다: {str(e)}'
        }, status=500)