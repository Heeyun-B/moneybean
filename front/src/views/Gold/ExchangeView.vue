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
            <div class="date-group">
              <select v-model="startYear" class="picker-select">
                <option value="" disabled>년도</option>
                <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
              </select>
              <select v-model="startMonth" class="picker-select">
                <option value="" disabled>월</option>
                <option v-for="m in months" :key="m" :value="m">{{ m }}</option>
              </select>
              <select v-model="startDay" class="picker-select">
                <option value="" disabled>일</option>
                <option v-for="d in startDays" :key="d" :value="d">{{ d }}</option>
              </select>
              
              <span class="sep">~</span>

              <select v-model="endYear" class="picker-select">
                <option value="" disabled>년도</option>
                <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
              </select>
              <select v-model="endMonth" class="picker-select">
                <option value="" disabled>월</option>
                <option v-for="m in months" :key="m" :value="m">{{ m }}</option>
              </select>
              <select v-model="endDay" class="picker-select">
                <option value="" disabled>일</option>
                <option v-for="d in endDays" :key="d" :value="d">{{ d }}</option>
              </select>

              <button @click="handleSearch" class="search-btn">검색</button>
            </div>
            <button @click="resetFilter" class="reset-mini-btn">초기화</button>
          </div>

          <div class="card-title">
            <span>{{ chartPeriodText }} 원화 시세 추이</span>
            <div class="price-badge">기간 평균: {{ averagePrice.toLocaleString() }} 원 / g</div>
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
            <input type="number" v-model="amount" @input="handleAmountInput" class="custom-input amount-input" placeholder="0" />
          </div>
          <div class="form-group">
            <label>현재 1g당 원화 시세</label>
            <div class="custom-input readonly-input">{{ currentPrice.toLocaleString() }} 원</div>
          </div>
          <div class="result-area">
            <label>예상 총 자산 가치</label>
            <div class="total-value-container">
              <div class="total-value">
                <span class="amount-text">{{ totalPrice }}</span>
                <span class="currency">원</span>
              </div>
              <div v-if="koreanValue" class="korean-summary">약 {{ koreanValue }}원</div>
            </div>
          </div>
          <div class="info-footer">
            <span class="wood-badge" @click="linkToMyAsset" style="cursor: pointer;">내 자산 연동</span>
            <p>보유하신 수량에 따른 현재 시점 원화 가치입니다.</p>
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

const route = useRoute();
const router = useRouter()
const asset = ref('gold');
const allRawData = ref([]);
const chartData = ref(null);
const chartKey = ref(0);
const currentPrice = ref(0);
const averagePrice = ref(0);
const amount = ref(1);
const totalPrice = ref("0")
const koreanValue = ref("")
const startYear = ref('');
const startMonth = ref('');
const startDay = ref('');
const endYear = ref('');
const endMonth = ref('');
const endDay = ref('');
const startDate = ref('');
const endDate = ref('');

const years = ['2023', '2024', '2025', '2026']
const months = Array.from({ length: 12 }, (_, i) => String(i + 1).padStart(2, '0'))
const getDaysInMonth = (year, month) => new Date(year, month, 0).getDate()

const startDays = computed(() => {
  const y = parseInt(startYear.value) || 2024;
  const m = parseInt(startMonth.value) || 1;
  return Array.from({ length: getDaysInMonth(y, m) }, (_, i) => String(i + 1).padStart(2, '0'));
});

const endDays = computed(() => {
  const y = parseInt(endYear.value) || 2024;
  const m = parseInt(endMonth.value) || 1;
  return Array.from({ length: getDaysInMonth(y, m) }, (_, i) => String(i + 1).padStart(2, '0'));
});

const assetTheme = computed(() => asset.value === 'gold' ? 'theme-gold' : 'theme-silver')
const chartPeriodText = computed(() => (startDate.value || endDate.value) ? '선택 기간' : '전체 기간')

const fetchData = async (type) => {
  asset.value = type;
  chartData.value = null 
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`http://127.0.0.1:8000/api/gold_prices/prices/`, {
      params: { asset: type },
      headers: { Authorization: token ? `Token ${token}` : '' }
    })
    const data = response.data.data.sort((a, b) => new Date(a.Date) - new Date(b.Date));
    allRawData.value = data;
    if (data.length > 0) {
      currentPrice.value = data[data.length - 1].price_krw_g;
    }
    applyFilter(); 
    calculate();
  } catch (error) {
    console.error('데이터 로드 실패:', error)
  }
}

const handleSearch = () => {
  const isStartIncomplete = !startYear.value || !startMonth.value || !startDay.value;
  const isEndIncomplete = !endYear.value || !endMonth.value || !endDay.value;

  // 하나라도 선택 안 된게 있으면 전체 기간 조회
  if (isStartIncomplete || isEndIncomplete) {
    startDate.value = '';
    endDate.value = '';
  } else {
    // 모두 선택되었을 때만 날짜 조합
    const sDate = `${startYear.value}-${startMonth.value}-${startDay.value}`;
    const eDate = `${endYear.value}-${endMonth.value}-${endDay.value}`;

    // 날짜 역전 방지
    if (new Date(sDate) > new Date(eDate)) {
      alert("시작 날짜가 종료 날짜보다 늦을 수 없습니다");
      return;
    }
    
    startDate.value = sDate;
    endDate.value = eDate;
  }

  // 필터 함수 직접 실행
  applyFilter();
};

const applyFilter = () => {
  if (!allRawData.value || allRawData.value.length === 0) return;

  let filtered = [];

  if (!startDate.value || !endDate.value) {
    // 날짜가 없으면 전체 데이터
    filtered = [...allRawData.value];
  } else {
    // 날짜가 있으면 기간 필터링
    const start = new Date(startDate.value);
    const end = new Date(endDate.value);
    
    filtered = allRawData.value.filter(item => {
      const itemDate = new Date(item.Date);
      return itemDate >= start && itemDate <= end;
    });
  }

  if (filtered.length > 0) {
    renderChart(filtered);
    const sum = filtered.reduce((acc, item) => acc + (item.price_krw_g || 0), 0);
    averagePrice.value = Math.floor(sum / filtered.length);
  } else {
    alert("해당 기간에 데이터가 없습니다.");
    resetFilter();
  }
};

const updateDateAndFilter = () => {
};

const renderChart = (data) => {
  const color = asset.value === 'gold' ? '#D4AF37' : '#9ea7ad'
  chartData.value = {
    labels: data.map(i => i.Date),
    datasets: [{
      borderColor: color,
      backgroundColor: asset.value === 'gold' ? 'rgba(212, 175, 55, 0.1)' : 'rgba(158, 167, 173, 0.1)',
      data: data.map(i => i.price_krw_g),
      tension: 0.4, fill: true, pointRadius: data.length > 60 ? 0 : 4
    }]
  }
  chartKey.value++
}

const calculate = () => {
  const total = (amount.value || 0) * currentPrice.value
  totalPrice.value = Math.floor(total).toLocaleString()
  koreanValue.value = formatKorean(Math.floor(total))
}

const formatKorean = (num) => {
  if (!num) return ""
  const units = ["", "만", "억", "조", "경"]
  let res = [], i = 0
  while (num > 0) {
    let p = num % 10000
    if (p > 0) res.unshift(p.toLocaleString() + units[i])
    num = Math.floor(num / 10000); i++
  }
  return res.join(" ")
}

const resetFilter = () => {
  startYear.value = ''; startMonth.value = ''; startDay.value = '';
  endYear.value = ''; endMonth.value = ''; endDay.value = '';
  startDate.value = '';
  endDate.value = '';

  if (allRawData.value.length > 0) {
    renderChart(allRawData.value);
    
    const sum = allRawData.value.reduce((acc, item) => acc + (item.price_krw_g || 0), 0);
    averagePrice.value = Math.floor(sum / allRawData.value.length);
  }
}

const handleAmountInput = () => {
  const maxAmount = 1000000000;
  if (amount.value > maxAmount) {
    alert("입력 가능한 최대 수량은 10억g입니다.");
    amount.value = maxAmount;
  }
  calculate();
}
const linkToMyAsset = () => router.push({ name: 'asset-create', query: { asset_type: asset.value, amount: amount.value, price: currentPrice.value } })
const chartOptions = { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { grid: { color: '#f0f0f0' } }, x: { grid: { display: false } } } }

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

.filter-container { margin-bottom: 25px; display: flex; align-items: center; justify-content: space-between; background: #f8f9fa; padding: 10px 15px; border-radius: 12px; border: 1px solid #eee; gap: 10px; }
.date-group { display: flex; align-items: center; gap: 4px; flex-shrink: 0; margin-right: 10px; }
.label-tag { font-size: 11px; color: #888; font-weight: bold; margin-right: 2px; flex-shrink: 0; }
.picker-select { border: 1px solid #ddd; background: #fff; font-size: 13px; color: #333; font-weight: 600; cursor: pointer; outline: none; padding: 4px 5px; border-radius: 6px; min-width: 65px; text-align: center; transition: 0.2s; }
.picker-select:hover { border-color: #00a651; color: #00a651; }
.sep { color: #aaa; font-weight: bold; padding: 0 2px; }
.date-separator { color: #ccc; font-weight: bold; flex-shrink: 0; padding: 0 2px; }

.search-btn { background: #00a651; color: white; border: none; padding: 6px 15px; border-radius: 8px; font-size: 13px;
  font-weight: bold; cursor: pointer; margin-left: 5px; transition: 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
.search-btn:hover { background: #008441; transform: translateY(-1px); }
.search-btn:active { transform: translateY(0); }

.reset-mini-btn { background: #473417; color: white; border: none; padding: 6px 15px; border-radius: 8px; font-size: 13px;
  font-weight: bold; cursor: pointer; margin-left: 5px; transition: 0.2s; white-space: nowrap; display: flex; align-items: center; gap: 4px; box-shadow: 0 2px 5px rgba(0, 166, 81, 0.2); }
.reset-mini-btn:hover { background: #795c34; color: white; transform: translateY(-1px); box-shadow: 0 4px 8px rgba(0, 166, 81, 0.3); }
.reset-mini-btn:active { transform: translateY(0); }

.form-group { margin-bottom: 20px; display: flex; flex-direction: column; }
label { font-size: 13px; font-weight: bold; color: #555; margin-bottom: 8px; }
.custom-input { padding: 15px; border: 1px solid #ddd; border-radius: 12px; font-size: 18px; outline: none; transition: 0.2s; width: 100%; box-sizing: border-box; }
.amount-input { border: 2px solid #eee; font-weight: bold; color: #333; }
.amount-input:focus { border-color: #00a651; }
.readonly-input { background: #f9f9f9; color: #888; border: 1px dashed #ccc; display: flex; align-items: center; }

/* 금액 넘침 방지 */
.result-area { background: #f1fcf4; border-radius: 15px; padding: 20px 10px; text-align: center; margin-top: 10px; 
  min-height: 140px; display: flex; flex-direction: column; justify-content: center; overflow: hidden; }
.total-value-container { display: flex; flex-direction: column; gap: 8px; width: 100%; }
.total-value { color: #00a651; font-weight: 900; display: flex; align-items: baseline; justify-content: center; width: 100%; gap: 4px; }
.amount-text { font-size: clamp(16px, 4vw, 26px); line-height: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex-shrink: 1; }
.korean-summary { font-size: 13px; color: #666; font-weight: 600; background: rgba(255, 255, 255, 0.5); padding: 4px 10px; 
  border-radius: 20px; display: inline-block; align-self: center; word-break: keep-all; }
.currency { font-size: 16px; color: #333; font-weight: 600; flex-shrink: 0; }

.info-footer { margin-top: 25px; text-align: center; }
.wood-badge { background: #8B4513; color: white; padding: 8px 12px; border-radius: 80px; font-size: 14px; display: inline-block; margin-bottom: 8px; }
.info-footer p { font-size: 12px; color: #999; }

.theme-gold .title { color: #B8860B; }
.theme-gold .result-area { border-left: 5px solid #D4AF37; }
.theme-silver .title { color: #607d8b; }
.theme-silver .result-area { border-left: 5px solid #C0C0C0; }

.loading-box { height: 450px; display: flex; align-items: center; justify-content: center; color: #999; }

@media (max-width: 450px) { 
  .amount-text { font-size: 18px; } 
  .main-layout { grid-template-columns: 1fr; }
}
</style>