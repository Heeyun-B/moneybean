import openai
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

        # 2. GPT 전달용 프롬프트 조립 (기존 가이드라인 유지)
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
## 💪 강점
## ⚠️ 개선이 필요한 부분
## 💡 맞춤 실행 제안
## 📈 기대 효과

**작성 가이드:**
- 친근하고 공감하는 톤으로 작성
- 구체적인 숫자와 비율 언급
- 전문 용어는 쉽게 풀어서 설명
"""

        # 3. GPT API 호출
        # gpt-4o 모델은 분석 능력이 매우 뛰어납니다.
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": "당신은 고객의 자산을 분석하여 최적의 금융 솔루션을 제공하는 AI 비서 '머니빈'입니다."},
                {"role": "user", "content": prompt_content}
            ],
            temperature=0.7
        )

        # 4. 결과 반환
        return Response({
            'success': True,
            'report': response.choices[0].message.content,
        })

    except Exception as e:
        return Response({
            'error': f'GPT 진단 중 오류가 발생했습니다: {str(e)}'
        }, status=500)