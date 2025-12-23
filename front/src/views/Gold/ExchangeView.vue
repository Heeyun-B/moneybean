<template>
  <div class="exchange-container" :class="assetTheme">
    <div class="header-area">
      <h1 class="title">
        <span v-if="asset === 'gold'">금 시세 정보</span>
        <span v-else>은 시세 정보</span>
      </h1>
      <p class="sub-text">머니빈이 제공하는 현물 시세를 확인하고 자산 가치를 계산해보세요.</p>
    </div>

    <div class="main-layout">
      <div class="left-section">
        <div class="chart-card">
          <div class="filter-container">
            <div class="date-inputs">
              <input type="date" v-model="startDate" @change="applyFilter" class="date-field">
              <span class="swash">~</span>
              <input type="date" v-model="endDate" @change="applyFilter" class="date-field">
            </div>
            <button @click="resetFilter" class="reset-btn">전체 기간</button>
            <p v-if="dateError" class="date-error-text">{{ dateError }}</p>
          </div>

          <div class="card-title">
            <span>📈 {{ chartPeriodText }} 시세 추이</span>
            <div class="price-badge">{{ currentPrice.toLocaleString() }} 원 / oz</div>
          </div>
          <div class="chart-wrapper" v-if="chartData">
            <Line :data="chartData" :options="chartOptions" :key="chartKey" />
          </div>
          <div v-else class="loading-box">시세 데이터를 불러오는 중...</div>
        </div>
      </div>

      <div class="right-section">
        <div class="input-card">
          <h3 class="card-title">💰 {{ asset === 'gold' ? '금' : '은' }} 가치 계산기</h3>
          
          <div class="form-group">
            <label>보유 수량 (온스/oz)</label>
            <input 
              type="number" 
              v-model="amount" 
              @input="calculate" 
              class="custom-input amount-input"
              placeholder="0" 
            />
          </div>

          <div class="form-group mb-large">
            <label>현재 1온스당 시세</label>
            <div class="custom-input readonly-input">
              {{ currentPrice.toLocaleString() }} 원
            </div>
          </div>

          <div class="result-area">
            <label>예상 총 자산 가치</label>
            <div class="total-value">
              <span class="amount-text">{{ totalPrice }}</span>
              <span class="currency">원</span>
            </div>
          </div>

          <div class="info-footer">
            <span class="wood-badge" @click="linkToMyAsset" style="cursor: pointer;">내 자산 연동</span>
            <p>보유하신 수량에 따른 현재 가치입니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const route = useRoute()
const router = useRouter()

const asset = ref('gold')
const allRawData = ref([])
const chartData = ref(null)
const chartKey = ref(0) 
const currentPrice = ref(0)
const amount = ref(1)
const totalPrice = ref("0")

// 기간 필터 상태
const startDate = ref('')
const endDate = ref('')
const dateError = ref('')

const assetTheme = computed(() => asset.value === 'gold' ? 'theme-gold' : 'theme-silver')
const chartPeriodText = computed(() => (startDate.value || endDate.value) ? '선택 기간' : '최근 30일')

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    y: { beginAtZero: false, grid: { color: '#f0f0f0' } },
    x: { grid: { display: false } }
  }
}

const fetchData = async (type) => {
  asset.value = type
  chartData.value = null 
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`http://127.0.0.1:8000/api/gold_prices/prices/`, {
      params: { asset: type },
      headers: { Authorization: `Token ${token}` }
    })
    
    allRawData.value = response.data.data.sort((a, b) => new Date(a.Date) - new Date(b.Date))
    applyFilter()

    const lastItem = allRawData.value[allRawData.value.length - 1]
    const lastPrice = lastItem['Close/Last'] || lastItem['close_last']
    currentPrice.value = parseFloat(String(lastPrice).replace(/,/g, ''))
    calculate()
  } catch (error) {
    console.error('데이터 로드 실패:', error)
  }
}

const applyFilter = () => {
  dateError.value = ''
  let filtered = [...allRawData.value]

  if (startDate.value && endDate.value && new Date(startDate.value) > new Date(endDate.value)) {
    dateError.value = '잘못된 날짜 선택: 시작일이 종료일보다 늦습니다.'
    return
  }

  if (startDate.value) filtered = filtered.filter(item => new Date(item.Date) >= new Date(startDate.value))
  if (endDate.value) filtered = filtered.filter(item => new Date(item.Date) <= new Date(endDate.value))
  
  // 날짜 선택 안했을 때 : 최근 30일만 보여주기
  if (!startDate.value && !endDate.value) filtered = filtered.slice(-30)

  renderChart(filtered)
}

const resetFilter = () => {
  startDate.value = ''; endDate.value = ''; applyFilter()
}

const renderChart = (data) => {
  const brandColor = asset.value === 'gold' ? '#D4AF37' : '#9ea7ad'
  chartData.value = {
    labels: data.map(item => item.Date),
    datasets: [{
      label: '시세',
      borderColor: brandColor,
      backgroundColor: asset.value === 'gold' ? 'rgba(212, 175, 55, 0.1)' : 'rgba(158, 167, 173, 0.1)',
      data: data.map(item => parseFloat(String(item['Close/Last'] || item['close_last']).replace(/,/g, ''))),
      tension: 0.4,
      fill: true,
      pointRadius: data.length > 60 ? 0 : 4
    }]
  }
  chartKey.value++
}

const calculate = () => {
  const total = amount.value * currentPrice.value
  totalPrice.value = Math.floor(total).toLocaleString()
}

const linkToMyAsset = () => {
  router.push({
    name: 'asset-create',
    query: { asset_type: asset.value, amount: amount.value, price: currentPrice.value }
  })
}

onMounted(() => fetchData(route.query.asset || 'gold'))
watch(() => route.query.asset, (newAsset) => { if (newAsset) fetchData(newAsset) })
</script>

<style scoped>
.exchange-container { max-width: 1100px; margin: 0 auto; padding: 40px 20px; }
.header-area { text-align: center; margin-bottom: 40px; }
.title { font-size: 32px; font-weight: 800; margin-bottom: 10px; }
.sub-text { color: #666; font-size: 15px; }
.main-layout { display: grid; grid-template-columns: 1fr 380px; gap: 30px; align-items: start; }
.chart-card, .input-card { background: white; border-radius: 20px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; }
.card-title { font-size: 18px; font-weight: bold; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f9f9f9; padding-bottom: 15px; }
.chart-wrapper { height: 450px; }
.price-badge { background: #f1fcf4; color: #00a651; padding: 5px 15px; border-radius: 50px; font-size: 14px; font-weight: bold; }

/* 기간 필터 스타일 (차트 카드 내부 상단) */
.filter-container { margin-bottom: 20px; display: flex; align-items: center; gap: 15px; flex-wrap: wrap; }
.date-inputs { display: flex; align-items: center; gap: 8px; }
.date-field { padding: 6px 10px; border: 1px solid #eee; border-radius: 8px; font-size: 13px; color: #555; }
.swash { color: #ccc; }
.reset-btn { background: #f5f5f5; border: none; padding: 6px 12px; border-radius: 8px; font-size: 12px; cursor: pointer; color: #666; }
.date-error-text { color: #ff5252; font-size: 12px; width: 100%; margin: 0; }

/* 계산기 스타일 */
.form-group { margin-bottom: 20px; display: flex; flex-direction: column; }
label { font-size: 13px; font-weight: bold; color: #555; margin-bottom: 8px; }
.custom-input { padding: 15px; border: 1px solid #ddd; border-radius: 12px; font-size: 18px; outline: none; transition: 0.2s; width: 100%; box-sizing: border-box; }
.amount-input { border: 2px solid #eee; font-weight: bold; color: #333; }
.amount-input:focus { border-color: #00a651; }
.readonly-input { background: #f9f9f9; color: #888; border: 1px dashed #ccc; display: flex; align-items: center; }
.result-area { background: #f1fcf4; border-radius: 15px; padding: 25px; text-align: center; margin-top: 10px; }
.total-value { color: #00a651; font-weight: 900; margin: 10px 0; display: flex; justify-content: center; align-items: baseline; }
.amount-text { font-size: 32px; }
.currency { font-size: 18px; margin-left: 5px; }
.info-footer { margin-top: 25px; text-align: center; }
.wood-badge { background: #8B4513; color: white; padding: 4px 12px; border-radius: 50px; font-size: 11px; display: inline-block; margin-bottom: 8px; }
.info-footer p { font-size: 12px; color: #999; }

.theme-gold .title { color: #B8860B; }
.theme-gold .result-area { border-left: 5px solid #D4AF37; }
.theme-silver .title { color: #607d8b; }
.theme-silver .result-area { border-left: 5px solid #C0C0C0; }

@media (max-width: 900px) { .main-layout { grid-template-columns: 1fr; } }
</style>