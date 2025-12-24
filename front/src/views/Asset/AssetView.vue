<template>
  <div class="asset-container">
    <h1>💰 내 자산 관리</h1>

    <div v-if="!isLoading && !store.isDataExists" class="empty-state">
      <div class="mascot-wrapper">
        <img src="@/assets/logo_bean.png" alt="머니빈" class="mascot-img">
      </div>
      <p class="empty-msg">아직 등록된 자산이 없네요!</p>
      <p class="sub-msg">내 자산을 입력하면 한눈에 볼 수 있어요.</p>
      <button @click="goToCreatePage" class="primary-btn">내 자산 입력하러 가기</button>
    </div>

    <div v-else-if="isLoading" class="skeleton-dashboard">
      <div class="summary-row">
        <SkeletonLoader height="120px" radius="16px" />
        <SkeletonLoader height="120px" radius="16px" />
        <SkeletonLoader height="120px" radius="16px" />
      </div>
      <div class="chart-section">
        <div class="skeleton-card"><SkeletonLoader height="300px" radius="16px" /></div>
        <div class="skeleton-card"><SkeletonLoader height="300px" radius="16px" /></div>
      </div>
      <SkeletonLoader height="80px" radius="16px" style="margin-bottom: 40px;" />
      <div class="skeleton-list">
        <SkeletonLoader height="40px" width="200px" style="margin-bottom: 20px;" />
        <SkeletonLoader v-for="n in 3" :key="n" height="60px" radius="8px" style="margin-bottom: 10px;" />
      </div>
    </div>

    <div v-else class="dashboard">
      
      <div class="summary-row">
        <div class="summary-card net-worth-card">
          <h3>순자산 (자산 - 부채)</h3>
          <p class="amount highlight">{{ store.netWorth.toLocaleString() }}원</p>
        </div>
        
        <div class="summary-card clickable-card" @click="scrollToSection('cash')">
          <h3>총 자산 <span>(▼ 목록 보기)</span></h3>
          <p class="amount asset-color">{{ store.totalAssets.toLocaleString() }}원</p>
        </div>

        <div class="summary-card clickable-card" @click="scrollToSection('debt')">
          <h3>총 부채 <span>(▼ 목록 보기)</span></h3>
          <p class="amount debt-color">{{ store.totalDebt.toLocaleString() }}원</p>
        </div>
      </div>

      <div class="chart-section">
        <div class="chart-card">
          <h3>자산 포트폴리오</h3>
          <div class="doughnut-wrapper">
            <div class="center-logo">
              <span class="floating-emoji">🌱</span>
            </div>
            <Doughnut v-if="doughnutData" :data="doughnutData" :options="doughnutOptions" />
          </div>
        </div>

        <div class="chart-card">
          <h3>자산/부채 현황</h3>
          <div class="bar-wrapper">
            <Bar v-if="barData" :data="barData" :options="barOptions" />
          </div>
        </div>
      </div>

      <div class="ai-section">
        <div class="ai-banner">
          <div class="ai-text">
            <h4>🤖 AI 금융 비서에게 진단받기</h4>
            <p>내 자산 포트폴리오를 분석하고 맞춤형 조언을 받아보세요.</p>
          </div>
          <button class="ai-btn" @click="handleAiDiagnosis" :disabled="isAiLoading">
            {{ isAiLoading ? '분석 중입니다... ⏳' : '진단 시작하기 🚀' }}
          </button>
        </div>

        <div v-if="aiReport" class="ai-result-card">
          <div class="markdown-body" v-html="renderedReport"></div>
          <button class="close-report" @click="aiReport = ''">접기</button>
        </div>
      </div>

      <div class="list-section">
        <div class="list-header-row">
          <h3>상세 자산 목록</h3>
          <div class="header-action-btns">
            <button @click="router.push({ name: 'exchange', query: { asset: 'gold' } })" class="exchange-btn">
              🪙 금/은 시세 확인
            </button>
            <button @click="goToCreatePage" class="edit-btn">목록 편집</button>
          </div>
        </div>

        <div class="hierarchical-list">
          <div 
            v-for="section in assetSections" 
            :key="section.key" 
            :id="`section-${section.key}`" 
            class="major-section"
          >
            <div class="major-header" :class="section.key">
              <span class="major-title">{{ section.label }}</span>
              <span class="major-total">{{ section.total.toLocaleString() }}원</span>
            </div>

            <div v-for="group in section.groups" :key="group.categoryId" class="sub-group">
              <div class="sub-header">
                <span class="sub-title">📂 {{ group.categoryName }}</span>
                <span class="sub-total">합계: {{ group.totalValue.toLocaleString() }}원</span>
              </div>
              <ul class="item-list">
                <li v-for="asset in group.items" :key="asset.id" class="asset-item">
                  <span class="asset-name">{{ asset.name }}</span>
                  <span class="asset-value">{{ Number(asset.current_value).toLocaleString() }}원</span>
                </li>
              </ul>
            </div>
            
            <div v-if="section.groups.length === 0" class="empty-section-msg">
              등록된 {{ section.label }}이 없습니다.
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAssetStore } from '@/stores/asset' // [수정] 파일명 변경 반영
import SkeletonLoader from '@/components/common/SkeletonLoader.vue' // [추가] 스켈레톤 컴포넌트

// 차트 라이브러리 설정
import { Chart as ChartJS, ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { Doughnut, Bar } from 'vue-chartjs'
import MarkdownIt from 'markdown-it'

ChartJS.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const store = useAssetStore()
const router = useRouter()
const md = new MarkdownIt()

// UI 상태 관리
const isLoading = ref(true)     // 초기 데이터 로딩 상태
const isAiLoading = ref(false)  // AI 진단 로딩 상태
const aiReport = ref('')

const renderedReport = computed(() => md.render(aiReport.value))

onMounted(async () => {
  isLoading.value = true
  
  try {
    // 병렬로 데이터 로드
    const [result] = await Promise.all([
      store.getAssets(),
      store.getCategories(),
      // UX를 위해 최소 0.6초간 스켈레톤 노출 (너무 빨리 깜빡이는 것 방지)
      new Promise(resolve => setTimeout(resolve, 600))
    ])
    
    if (result === 'NO_TOKEN' || result === 'AUTH_ERROR') {
      alert('로그인이 필요한 서비스입니다.')
      router.push({ name: 'login' })
    }
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
})

const goToCreatePage = () => {
  router.push({ name: 'asset-create' })
}

const handleAiDiagnosis = async () => {
  if (!confirm('AI 진단을 시작하시겠습니까? (약 3초 소요)')) return

  isAiLoading.value = true
  aiReport.value = ''

  // 백엔드 AI가 분석하기 좋게 가공된 데이터 꾸러미(Payload)
  const payload = {
    totalAssets: store.totalAssets,
    totalCash: store.totalCash,
    totalInvest: store.totalInvest,
    totalDebt: store.totalDebt,
    netWorth: store.netWorth,
    income: store.financialInfo.income,
    expense: store.financialInfo.expense,
    // Vue에서 computed로 만든 계층 구조 데이터를 그대로 보냅니다.
    sections: assetSections.value 
  }

  try {
    // 스토어 함수 호출 시 위에서 만든 payload를 전달
    const result = await store.getAiDiagnosis(payload)
    aiReport.value = result
  } catch (error) {
    console.error(error)
    alert('AI 서버 연결에 실패했습니다. 잠시 후 다시 시도해주세요.')
  } finally {
    isAiLoading.value = false
  }
}

const scrollToSection = (key) => {
  const element = document.getElementById(`section-${key}`)
  if (element) {
    const yOffset = -80 // 네비바 높이 고려
    const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset
    window.scrollTo({ top: y, behavior: 'smooth' })
  }
}

// --- 차트 및 리스트 데이터 가공 로직 (기존 유지) ---
const groupAssets = (assets) => {
  if (!assets || assets.length === 0) return []
  const groups = {}
  assets.forEach(asset => {
    const catId = asset.category
    if (!groups[catId]) {
      const catName = store.categories.find(c => c.id === catId)?.name || '기타'
      groups[catId] = { categoryId: catId, categoryName: catName, totalValue: 0, items: [] }
    }
    groups[catId].items.push(asset)
    groups[catId].totalValue += Number(asset.current_value)
  })
  return Object.values(groups)
}

const assetSections = computed(() => [
  { key: 'cash', label: '현금성 자산', total: store.totalCash, groups: groupAssets(store.cashAssets) },
  { key: 'invest', label: '투자 자산', total: store.totalInvest, groups: groupAssets(store.investAssets) },
  { key: 'debt', label: '부채', total: store.totalDebt, groups: groupAssets(store.debtAssets) }
])

const doughnutData = computed(() => {
  if (!store.totalAssets) return null
  return {
    labels: ['현금성 자산', '투자 자산'],
    datasets: [{
      backgroundColor: ['#00a651', '#2979FF'], 
      data: [store.totalCash, store.totalInvest],
      borderWidth: 0,
      hoverOffset: 10
    }]
  }
})

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '70%',
  layout: {
    padding: 20
  },
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        padding: 20,
        usePointStyle: true,
        font: { family: "'Pretendard', sans-serif", size: 12 }
      }
    },
    tooltip: {
      enabled: true,
      backgroundColor: 'rgba(0, 0, 0, 0.9)',
      titleFont: { size: 14, weight: 'bold' },
      bodyFont: { size: 13 },
      padding: 15,
      cornerRadius: 10,
      displayColors: false,
      
      callbacks: {
        // 1. 제목: 섹션 이름 + 총액 + 퍼센트
        title: (tooltipItems) => {
          const item = tooltipItems[0]
          const total = item.dataset.data.reduce((a, b) => a + b, 0)
          const value = item.raw
          const percentage = ((value / total) * 100).toFixed(1) + '%'
          return `${item.label} : ${percentage}`
        },
        // 2. 내용: 해당 섹션의 상세 자산 목록 나열
        label: (context) => {
          return ` 총액: ${Number(context.raw).toLocaleString()}원`
        },
        afterBody: (tooltipItems) => {
          const index = tooltipItems[0].dataIndex
          // 0번 인덱스면 현금성 자산, 1번이면 투자 자산
          const targetAssets = index === 0 ? store.cashAssets : store.investAssets
          
          if (!targetAssets || targetAssets.length === 0) return []

          // 자산 목록을 금액 순으로 정렬해서 상위 5개만 보여주거나 전체 보여주기
          const sortedList = [...targetAssets].sort((a, b) => b.current_value - a.current_value)
          
          const lines = ['----------------'] // 구분선
          
          sortedList.forEach(asset => {
             lines.push(`• ${asset.name}: ${Number(asset.current_value).toLocaleString()}원`)
          })
          
          return lines
        }
      }
    }
  },
  animation: { animateScale: true, animateRotate: true }
}

const barData = computed(() => ({
  labels: ['총 자산', '총 부채', '순자산'],
  datasets: [{
    label: '금액',
    data: [store.totalAssets, store.totalDebt, store.netWorth],
    backgroundColor: ['#00a651', '#FF8A65', '#42A5F5'],
    borderRadius: 6,
    barThickness: 50
  }]
}))

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    y: { beginAtZero: true, grid: { color: '#f5f5f5' } },
    x: { grid: { display: false } }
  }
}
</script>

<style scoped>
.asset-container { max-width: 900px; margin: 0 auto; padding: 40px 20px; color: #333; }
h1 { text-align: center; margin-bottom: 40px; font-size: 26px; font-weight: 800; }

/* 스켈레톤 레이아웃 */
.skeleton-dashboard { animation: fadeIn 0.5s ease; }
.skeleton-card { background: #fff; padding: 20px; border-radius: 16px; border: 1px solid #f0f0f0; }

/* Summary Cards */
.summary-row { display: grid; grid-template-columns: 1.4fr 1fr 1fr; gap: 20px; margin-bottom: 40px; }
.summary-card {
  background: white; padding: 25px; border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.04); border: 1px solid #f0f0f0;
  display: flex; flex-direction: column; justify-content: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.clickable-card { cursor: pointer; }
.clickable-card:hover { transform: translateY(-4px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
.clickable-card h3 span { font-size: 11px; color: #999; margin-left: 5px; font-weight: normal; }

.net-worth-card {
  background: linear-gradient(135deg, #00a651 0%, #008e45 100%);
  color: white; border: none; box-shadow: 0 8px 20px rgba(0, 166, 81, 0.25);
}
.summary-card h3 { margin: 0 0 8px 0; font-size: 14px; opacity: 0.8; font-weight: normal; }
.net-worth-card h3 { opacity: 0.95; color: #E0F2F1; }
.amount { font-size: 22px; font-weight: 800; margin: 0; }
.amount.highlight { font-size: 30px; }
.amount.asset-color { color: #00a651; }
.amount.debt-color { color: #FF7043; }

/* Charts */
.chart-section { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }
.chart-card {
  background: white; padding: 25px; border-radius: 16px;
  border: 1px solid #f0f0f0; box-shadow: 0 4px 15px rgba(0,0,0,0.03); text-align: center;
}
.doughnut-wrapper { 
  position: relative; 
  height: 300px; /* 차트 높이를 조금 더 넉넉하게 줌 */
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.bar-wrapper { position: relative; height: 240px; }
.center-logo {
  position: absolute; 
  top: 45%; /* 범례가 아래로 내려갔으므로 중앙점을 살짝 위로 조정 */
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60px; height: 60px; 
  display: flex; align-items: center; justify-content: center; 
  
  /* [중요] 마우스 이벤트를 통과시켜서 뒤에 있는 차트(툴팁)가 반응하게 함 */
  pointer-events: none; 
  z-index: 0; /* 차트보다 뒤로 보낼 필요는 없지만, 툴팁 간섭 최소화 */
}
.floating-emoji { font-size: 45px; animation: float 3s ease-in-out infinite; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1)); }

/* 차트 캔버스 (Chart.js가 생성하는 canvas) */
:deep(canvas) {
  z-index: 10; /* 캔버스가 로고보다 위에 있어야 함 (그래야 툴팁이 로고 위로 올라옴) */
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
  100% { transform: translateY(0px); }
}

/* AI Section */
.ai-section { margin-bottom: 40px; }
.ai-banner {
  background: linear-gradient(95deg, #E3F2FD 0%, #BBDEFB 100%);
  border-radius: 16px; padding: 25px 30px;
  display: flex; justify-content: space-between; align-items: center;
  box-shadow: 0 4px 15px rgba(33, 150, 243, 0.15); border: 1px solid #BBDEFB;
}
.ai-text h4 { margin: 0 0 5px 0; font-size: 18px; color: #1565C0; }
.ai-text p { margin: 0; font-size: 14px; color: #555; }
.ai-btn {
  background-color: #1976D2; color: white; padding: 12px 24px;
  border: none; border-radius: 8px; font-weight: bold; cursor: pointer;
  transition: transform 0.2s, background-color 0.2s; box-shadow: 0 4px 10px rgba(25, 118, 210, 0.2);
}
.ai-btn:hover:not(:disabled) { background-color: #1565C0; transform: translateY(-2px); }
.ai-btn:disabled { background-color: #90CAF9; cursor: not-allowed; }

.ai-result-card {
  margin-top: 20px; background: #fff; border: 1px solid #e0e0e0;
  border-radius: 16px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); text-align: left;
  animation: fadeIn 0.5s ease-in-out;
}
.close-report {
  margin-top: 20px; background: #f5f5f5; border: none; padding: 10px 20px;
  border-radius: 8px; cursor: pointer; font-weight: bold; color: #666; width: 100%;
}
.close-report:hover { background: #e0e0e0; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Markdown Styles */
:deep(.markdown-body h1) { font-size: 22px; color: #00a651; margin-bottom: 15px; border-bottom: 2px solid #eee; padding-bottom: 10px; }
:deep(.markdown-body h2) { font-size: 18px; color: #333; margin-top: 20px; margin-bottom: 10px; }
:deep(.markdown-body p) { line-height: 1.6; color: #555; margin-bottom: 10px; }

/* List Section */
.list-section { background: white; border-radius: 20px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); }
.list-header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; padding-bottom: 10px; border-bottom: 1px solid #eee; }
.header-action-btns { display: flex; gap: 10px; }
.exchange-btn { background: #fff; border: 1px solid #D4AF37; padding: 6px 14px; border-radius: 8px; font-size: 13px; cursor: pointer; color: #B8860B; font-weight: bold; transition: 0.2s; }
.exchange-btn:hover { background: #FFFDE7; transform: translateY(-1px); }
.edit-btn { background: white; border: 1px solid #ddd; padding: 6px 14px; border-radius: 8px; font-size: 13px; cursor: pointer; color: #555; }
.edit-btn { background: white; border: 1px solid #ddd; padding: 6px 14px; border-radius: 8px; font-size: 13px; cursor: pointer; color: #555; }
.edit-btn:hover { background: #f5f5f5; color: #111; }

.major-section { margin-bottom: 40px; scroll-margin-top: 20px; }
.major-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 2px solid #333; margin-bottom: 15px; }
.major-header.cash { border-bottom-color: #00a651; color: #00695C; }
.major-header.invest { border-bottom-color: #2979FF; color: #1565C0; }
.major-header.debt { border-bottom-color: #FF8A65; color: #D84315; }
.major-title { font-size: 18px; font-weight: 800; }
.major-total { font-size: 18px; font-weight: bold; }

.sub-group { margin-bottom: 20px; padding-left: 10px; }
.sub-header { display: flex; justify-content: space-between; align-items: center; background-color: #f9f9f9; padding: 8px 12px; border-radius: 8px; margin-bottom: 8px; }
.sub-title { font-size: 14px; font-weight: 600; color: #444; }
.asset-item { display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; border-bottom: 1px solid #f0f0f0; font-size: 15px; }
.asset-value { font-weight: bold; color: #333; }
.empty-section-msg { color: #999; font-size: 13px; padding: 10px; text-align: center; background: #fafafa; border-radius: 8px; }

/* Empty State & Mobile */
.empty-state { text-align: center; padding: 60px 20px; background: #f9f9f9; border-radius: 20px; }
.mascot-img { width: 100px; margin-bottom: 20px; }
.primary-btn { background-color: #00a651; color: white; padding: 12px 30px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; }

@media (max-width: 768px) {
  .summary-row, .chart-section { grid-template-columns: 1fr; }
  .center-logo { left: 50%; }
  .ai-banner { flex-direction: column; text-align: center; gap: 15px; }
  .ai-btn { width: 100%; }
}
</style>