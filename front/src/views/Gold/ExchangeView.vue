<template>
  <div class="exchange-container" :class="assetTheme">
    <div class="header-area">
      <h1 class="title">
        <span v-if="asset === 'gold'">금 시세 정보</span>
        <span v-else>은 시세 정보</span>
      </h1>
      <p class="sub-text">머니빈이 제공하는 실시간 원화 환산 시세를 확인하고 자산 가치를 계산해보세요.</p>
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
            <span>📈 {{ chartPeriodText }} 원화 시세 추이</span>
            <div class="price-badge">{{ currentPrice.toLocaleString() }} 원 / g</div>
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
            <label>보유 수량 (그램/g)</label>
            <input 
              type="number" 
              v-model="amount" 
              @input="handleAmountInput" 
              class="custom-input amount-input"
              placeholder="0" 
              max="1000000000"
            />
          </div>

          <div class="form-group mb-large">
            <label>현재 1g당 원화 시세</label>
            <div class="custom-input readonly-input">
              {{ currentPrice.toLocaleString() }} 원
            </div>
          </div>

          <div class="result-area">
            <label>예상 총 자산 가치</label>
            <div class="total-value-container">
              <div class="total-value">
                <span class="amount-text">{{ totalPrice }}</span>
                <span class="currency">원</span>
              </div>
              <div v-if="koreanValue" class="korean-summary">
                  약 {{ koreanValue }}원
                </div>
              </div>
          </div>

          <div class="info-footer">
            <span class="wood-badge" @click="linkToMyAsset" style="cursor: pointer;">내 자산 연동</span>
            <p>보유하신 수량에 따른 현재 원화 가치입니다.</p>
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

const startDate = ref('')
const endDate = ref('')
const dateError = ref('')
const koreanValue = ref("");

const assetTheme = computed(() => asset.value === 'gold' ? 'theme-gold' : 'theme-silver')
const chartPeriodText = computed(() => (startDate.value || endDate.value) ? '선택 기간' : '전체 기간')

const linkToMyAsset = () => {
  router.push({
    name: 'asset-create',
    query: { asset_type: asset.value, amount: amount.value, price: currentPrice.value }
  })
}


const handleAmountInput = () => {
  const maxAmount = 1000000000;
  if (amount.value > maxAmount) {
    amount.value = maxAmount;
    alert("최대 입력 가능한 수량은 10억g입니다.");
  }
  calculate();
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { 
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (context) => `${context.parsed.y.toLocaleString()} 원/g`
      }
    }
  },
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
      headers: { Authorization: token ? `Token ${token}` : '' }
    })
    
    allRawData.value = response.data.data.sort((a, b) => new Date(a.Date) - new Date(b.Date))
    applyFilter()

    const lastItem = allRawData.value[allRawData.value.length - 1]
    currentPrice.value = lastItem.price_krw_g || 0
    calculate()
  } catch (error) {
    console.error('데이터 로드 실패:', error)
  }
}

const applyFilter = () => {
  dateError.value = ''
  let filtered = [...allRawData.value]
  if (startDate.value && endDate.value && new Date(startDate.value) > new Date(endDate.value)) {
    dateError.value = '시작일이 종료일보다 늦습니다.'
    return
  }
  if (startDate.value) {
    filtered = filtered.filter(item => new Date(item.Date) >= new Date(startDate.value))
  }
  if (endDate.value) {
    filtered = filtered.filter(item => new Date(item.Date) <= new Date(endDate.value))
  }
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
      label: '원화 시세(g)',
      borderColor: brandColor,
      backgroundColor: asset.value === 'gold' ? 'rgba(212, 175, 55, 0.1)' : 'rgba(158, 167, 173, 0.1)',
      data: data.map(item => item.price_krw_g),
      tension: 0.4,
      fill: true,
      pointRadius: data.length > 60 ? 0 : 4
    }]
  }
  chartKey.value++
}

const formatKoreanAmount = (num) => {
  if (!num || num === 0) return "";
  const unitWords = ["", "만", "억", "조", "경"];
  let result = [];
  let unitIndex = 0;

  while (num > 0) {
    let part = num % 10000;
    if (part > 0) {
      result.unshift(part.toLocaleString() + unitWords[unitIndex]);
    }
    num = Math.floor(num / 10000);
    unitIndex++;
  }
  return result.join(" ");
};

const calculate = () => {
  if (!amount.value || amount.value < 0) {
    totalPrice.value = "0";
    koreanValue.value = "";
    return;
  }
  const total = amount.value * currentPrice.value;
  totalPrice.value = Math.floor(total).toLocaleString();
  koreanValue.value = formatKoreanAmount(Math.floor(total));
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

.filter-container { margin-bottom: 20px; display: flex; align-items: center; gap: 15px; flex-wrap: wrap; }
.date-inputs { display: flex; align-items: center; gap: 8px; }
.date-field { padding: 6px 10px; border: 1px solid #eee; border-radius: 8px; font-size: 13px; color: #555; }
.swash { color: #ccc; }
.reset-btn { background: #f5f5f5; border: none; padding: 6px 12px; border-radius: 8px; font-size: 12px; cursor: pointer; color: #666; }
.date-error-text { color: #ff5252; font-size: 12px; width: 100%; margin: 0; }

.form-group { margin-bottom: 20px; display: flex; flex-direction: column; }
label { font-size: 13px; font-weight: bold; color: #555; margin-bottom: 8px; }
.custom-input { padding: 15px; border: 1px solid #ddd; border-radius: 12px; font-size: 18px; outline: none; transition: 0.2s; width: 100%; box-sizing: border-box; }
.amount-input { border: 2px solid #eee; font-weight: bold; color: #333; }
.amount-input:focus { border-color: #00a651; }
.readonly-input { background: #f9f9f9; color: #888; border: 1px dashed #ccc; display: flex; align-items: center; }

/* 금액 넘침 방지 스타일 */
.result-area { background: #f1fcf4; border-radius: 15px; padding: 25px; text-align: center; margin-top: 10px; min-height: 140px; display: flex; flex-direction: column; justify-content: center; }
.total-value-container { display: flex; flex-direction: column; gap: 8px; }
.total-value { color: #00a651; font-weight: 900; display: flex;  align-items: baseline; justify-content: center; white-space: nowrap; width: 100%; overflow: hidden; gap: 2px; }
.amount-text { font-size: 28px;  line-height: 1; }
.korean-summary { font-size: 14px; color: #666; font-weight: 600; background: rgba(255, 255, 255, 0.5); padding: 4px 10px; border-radius: 20px; display: inline-block; align-self: center; }
.currency { font-size: 16px; margin-left: 2px; color: #333; font-weight: 600; line-height: 1; position: relative; bottom: 0px; }

.info-footer { margin-top: 25px; text-align: center; }
.wood-badge { background: #8B4513; color: white; padding: 4px 12px; border-radius: 50px; font-size: 11px; display: inline-block; margin-bottom: 8px; }
.info-footer p { font-size: 12px; color: #999; }

.theme-gold .title { color: #B8860B; }
.theme-gold .result-area { border-left: 5px solid #D4AF37; }
.theme-silver .title { color: #607d8b; }
.theme-silver .result-area { border-left: 5px solid #C0C0C0; }

.loading-box { height: 450px; display: flex; align-items: center; justify-content: center; color: #999; }

@media (max-width: 400px) { .amount-text { font-size: 20px; } }
</style>