<template>
  <div class="asset-container">
    <h1>💰 내 자산 관리</h1>

    <div v-if="!store.isDataExists" class="empty-state">
      <div class="mascot-wrapper">
        <img src="@/assets/logo_bean.png" alt="머니빈" class="mascot-img">
      </div>
      <p class="empty-msg">아직 등록된 자산이 없네요!</p>
      <p class="sub-msg">내 자산을 입력하면 한눈에 볼 수 있어요.</p>
      <button @click="goToCreatePage" class="primary-btn">내 자산 입력하러 가기</button>
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
          <button class="ai-btn" @click="handleAiDiagnosis" :disabled="isLoading">
            {{ isLoading ? '분석 중입니다... ⏳' : '진단 시작하기 🚀' }}
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
          <button @click="goToCreatePage" class="edit-btn">목록 편집</button>
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
import { useAssetStore } from '@/stores/assetStore'
import { useRouter } from 'vue-router'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { Doughnut, Bar } from 'vue-chartjs'
// [NEW] 마크다운 렌더러
import MarkdownIt from 'markdown-it'

ChartJS.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const store = useAssetStore()
const router = useRouter()
const isReady = ref(false)
const md = new MarkdownIt()

// [NEW] AI UI 상태 관리
const isLoading = ref(false)
const aiReport = ref('')

// [NEW] 마크다운 -> HTML 변환
const renderedReport = computed(() => md.render(aiReport.value))

onMounted(async () => {
  await store.getCategories()
  const result = await store.getAssets()
  
  if (result === 'NO_TOKEN' || result === 'AUTH_ERROR') {
    window.alert('로그인이 필요한 서비스입니다.')
    router.push({ name: 'login' })
    return
  }
  isReady.value = true
})

const goToCreatePage = () => {
  router.push({ name: 'asset-create' })
}

// [NEW] AI 진단 핸들러
const handleAiDiagnosis = async () => {
  if (!confirm('AI 진단을 시작하시겠습니까? (약 3초 소요)')) return

  isLoading.value = true
  aiReport.value = '' // 이전 결과 초기화

  try {
    // 스토어의 가짜(Mock) API 호출
    const result = await store.getAiDiagnosis()
    aiReport.value = result // 결과 저장
  } catch (error) {
    alert('AI 서버 연결에 실패했습니다. 잠시 후 다시 시도해주세요.')
  } finally {
    isLoading.value = false // 로딩 종료
  }
}

// 스크롤 이동 함수
const scrollToSection = (key) => {
  const element = document.getElementById(`section-${key}`)
  if (element) {
    const yOffset = -20 
    const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset
    window.scrollTo({ top: y, behavior: 'smooth' })
  }
}

// --- 데이터 그룹화 헬퍼 ---
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

// --- [차트 1] 도넛 차트 ---
const doughnutData = computed(() => {
  if (!store.totalAssets) return null
  return {
    labels: ['현금성 자산', '투자 자산'],
    datasets: [{
      backgroundColor: ['#00a651', '#2979FF'], 
      data: [store.totalCash, store.totalInvest],
      borderWidth: 0,
      hoverOffset: 6
    }]
  }
})

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '70%',
  plugins: {
    legend: {
      position: 'right',
      labels: {
        boxWidth: 12, padding: 20, font: { size: 12, family: "'Noto Sans KR', sans-serif" },
        generateLabels: (chart) => {
          const data = chart.data
          if (data.labels.length && data.datasets.length) {
            const dataset = data.datasets[0]
            const total = dataset.data.reduce((acc, val) => acc + val, 0)
            return data.labels.map((label, i) => {
              const value = dataset.data[i]
              const percentage = total > 0 ? ((value / total) * 100).toFixed(1) + '%' : '0%'
              return {
                text: `${label} (${percentage})`,
                fillStyle: dataset.backgroundColor[i],
                hidden: isNaN(value) || chart.getDatasetMeta(0).data[i].hidden,
                index: i
              }
            })
          }
          return []
        }
      }
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const value = context.raw || 0
          const total = context.chart._metasets[context.datasetIndex].total
          const percentage = ((value / total) * 100).toFixed(1) + '%'
          return ` 총액: ${Number(value).toLocaleString()}원 (${percentage})`
        },
        afterBody: (context) => {
          const index = context[0].dataIndex
          const assets = index === 0 ? store.cashAssets : store.investAssets
          if (!assets || assets.length === 0) return []
          const lines = ['----------------']
          assets.forEach(asset => {
            lines.push(`• ${asset.name}: ${Number(asset.current_value).toLocaleString()}원`)
          })
          return lines
        }
      },
      backgroundColor: 'rgba(0, 0, 0, 0.85)',
      padding: 12, cornerRadius: 8, titleFont: { size: 14 }, bodyFont: { size: 13 }, displayColors: true
    }
  },
  animation: { animateScale: true, animateRotate: true }
}

// --- [차트 2] 막대 차트 ---
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
  plugins: {
    legend: { display: false },
    tooltip: { callbacks: { label: (c) => ` ${Number(c.raw).toLocaleString()}원` } }
  },
  scales: {
    y: {
      beginAtZero: true, grid: { color: '#f5f5f5' },
      ticks: { callback: (v) => v >= 10000 ? (v/10000).toFixed(0)+'만' : v }
    },
    x: { grid: { display: false } }
  }
}
</script>

<style scoped>
.asset-container { max-width: 900px; margin: 0 auto; padding: 40px 20px; color: #333; }
h1 { text-align: center; margin-bottom: 40px; font-size: 26px; font-weight: 800; }

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
.chart-card h3 { margin-bottom: 20px; font-size: 16px; color: #444; }

/* 도넛 차트 중앙 새싹 효과 */
.doughnut-wrapper, .bar-wrapper { position: relative; height: 240px; }
.center-logo {
  position: absolute; top: 50%; left: 30%;
  transform: translate(-50%, -50%);
  width: 60px; height: 60px; 
  display: flex; align-items: center; justify-content: center; 
  pointer-events: none; z-index: 10;
}
.floating-emoji {
  font-size: 45px;
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
}
@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
  100% { transform: translateY(0px); }
}

/* [NEW] AI Section 스타일 */
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
.ai-btn:disabled { background-color: #90CAF9; cursor: not-allowed; transform: none; box-shadow: none; }

/* [NEW] AI 결과 카드 스타일 */
.ai-result-card {
  margin-top: 20px;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  text-align: left;
  animation: fadeIn 0.5s ease-in-out;
}

.close-report {
  margin-top: 20px;
  background: #f5f5f5;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  color: #666;
  width: 100%;
  transition: background 0.2s;
}
.close-report:hover { background: #e0e0e0; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 마크다운 렌더링 스타일 */
:deep(.markdown-body h1) { font-size: 22px; color: #00a651; margin-bottom: 15px; border-bottom: 2px solid #eee; padding-bottom: 10px; }
:deep(.markdown-body h2) { font-size: 18px; color: #333; margin-top: 20px; margin-bottom: 10px; }
:deep(.markdown-body p) { line-height: 1.6; color: #555; margin-bottom: 10px; }
:deep(.markdown-body li) { margin-bottom: 5px; color: #444; }
:deep(.markdown-body strong) { color: #00a651; }

/* List Section */
.list-section { background: white; border-radius: 20px; padding: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); }
.list-header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; padding-bottom: 10px; border-bottom: 1px solid #eee; }
.edit-btn { background: white; border: 1px solid #ddd; padding: 6px 14px; border-radius: 8px; font-size: 13px; cursor: pointer; color: #555; }
.edit-btn:hover { background: #f5f5f5; color: #111; }

.major-section { margin-bottom: 40px; scroll-margin-top: 20px; }
.major-section:last-child { margin-bottom: 0; }
.major-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 2px solid #333; margin-bottom: 15px; }
.major-header.cash { border-bottom-color: #00a651; color: #00695C; }
.major-header.invest { border-bottom-color: #2979FF; color: #1565C0; }
.major-header.debt { border-bottom-color: #FF8A65; color: #D84315; }
.major-title { font-size: 18px; font-weight: 800; }
.major-total { font-size: 18px; font-weight: bold; }

.sub-group { margin-bottom: 20px; padding-left: 10px; }
.sub-header { display: flex; justify-content: space-between; align-items: center; background-color: #f9f9f9; padding: 8px 12px; border-radius: 8px; margin-bottom: 8px; }
.sub-title { font-size: 14px; font-weight: 600; color: #444; }
.sub-total { font-size: 13px; color: #777; font-weight: 500; }
.item-list { list-style: none; padding: 0; margin: 0; }
.asset-item { display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; border-bottom: 1px solid #f0f0f0; font-size: 15px; }
.asset-item:last-child { border-bottom: none; }
.asset-name { color: #333; }
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