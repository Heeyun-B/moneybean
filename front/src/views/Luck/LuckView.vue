<template>
  <div class="luck-page">
    <div class="luck-card">
      <StandardLoader v-if="loading" :message="loadingMessage" />

      <template v-else>
        <div v-if="!hasBirthDate" class="registration-form">
          <h1 class="page-title">🎂 생년월일 등록</h1>
          <p class="form-desc">정확한 금전운 분석을 위해 최초 1회 등록이 필요합니다.</p>
          
          <div class="select-group">
            <select v-model="birth.year" class="luck-select">
              <option value="" disabled>년도</option>
              <option v-for="y in years" :key="y" :value="y">{{ y }}년</option>
            </select>
            <select v-model="birth.month" class="luck-select">
              <option value="" disabled>월</option>
              <option v-for="m in 12" :key="m" :value="m">{{ m }}월</option>
            </select>
            <select v-model="birth.day" class="luck-select">
              <option value="" disabled>일</option>
              <option v-for="d in 31" :key="d" :value="d">{{ d }}일</option>
            </select>
          </div>

          <button class="action-btn" :disabled="!isDateValid" @click="handleRegister">
            저장하고 금전운 확인하기
          </button>
        </div>

        <div v-else-if="fortune" class="result-area">
          <h1 class="page-title">✨ 오늘의 금전운 리포트</h1>

          <div class="gauge-section">
            <svg class="gauge-svg" viewBox="0 0 100 100">
              <circle class="bg" cx="50" cy="50" r="45"></circle>
              <circle class="meter" cx="50" cy="50" r="45" :style="gaugeStyle"></circle>
            </svg>
            <div class="gauge-text">
              <span class="score">{{ fortune.luck_index }}%</span>
            </div>
            <p class="summary">{{ fortune.summary }}</p>
          </div>

          <div class="report-list">
            <div v-for="(item, idx) in fortune.details" :key="idx" class="report-item">
              <button class="report-header" @click="activeIdx = activeIdx === idx ? null : idx">
                <span class="header-title">{{ item.title }}</span>
                <span class="arrow">{{ activeIdx === idx ? '▲' : '▼' }}</span>
              </button>
              <div v-show="activeIdx === idx" class="report-content">
                <div v-if="item.title.includes('가이드')" class="guide-box">
                  {{ item.content }}
                </div>
                <p v-else class="long-text">{{ item.content }}</p>
              </div>
            </div>
          </div>

          <button class="retry-btn" @click="fetchFortuneData">운세 다시 받기</button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { getLuckFortune } from '@/api/luck'
import { getUserProfile, updateProfile } from '@/api/auth'
import StandardLoader from '@/components/common/StandardLoader.vue'

const loading = ref(true)
const loadingMessage = ref('사용자 정보를 확인하고 있습니다...')
const fortune = ref(null)
const hasBirthDate = ref(false)
const activeIdx = ref(0)

// 날짜 선택기 데이터
const birth = reactive({ year: '', month: '', day: '' })
const years = Array.from({ length: 100 }, (_, i) => 2025 - i)
const isDateValid = computed(() => birth.year && birth.month && birth.day)

// 게이지 스타일
const gaugeStyle = computed(() => {
  const radius = 45
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (circumference * (fortune.value?.luck_index || 0)) / 100
  return { strokeDasharray: circumference, strokeDashoffset: offset }
})

// 초기 로드: 프로필 체크
onMounted(async () => {
  try {
    const profile = await getUserProfile()
    if (profile.birth_date) {
      hasBirthDate.value = true
      await fetchFortuneData()
    } else {
      hasBirthDate.value = false
      loading.value = false
    }
  } catch (err) {
    loading.value = false
  }
})

// 생년월일 등록 및 운세 호출
const handleRegister = async () => {
  loadingMessage.value = '생년월일을 저장하고 운세를 분석 중입니다...'
  loading.value = true
  try {
    const dateStr = `${birth.year}-${String(birth.month).padStart(2, '0')}-${String(birth.day).padStart(2, '0')}`
    await updateProfile({ birth_date: dateStr })
    hasBirthDate.value = true
    await fetchFortuneData()
  } catch (err) {
    alert('정보 저장에 실패했습니다.')
    loading.value = false
  }
}

const fetchFortuneData = async () => {
  loadingMessage.value = 'AI 머니빈이 만세력을 분석하고 있습니다...'
  loading.value = true
  try {
    const data = await getLuckFortune()
    if (data.success) {
      fortune.value = data
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.luck-page { max-width: 700px; margin: 0 auto; padding: 40px 20px; font-family: 'GmarketSansMedium'; }
.luck-card { background: #fff; border-radius: 24px; padding: 50px; box-shadow: 0 10px 40px rgba(0,0,0,0.06); min-height: 400px; }
.page-title { text-align: center; color: #00a651; margin-bottom: 20px; font-weight: 800; }

/* 입력 폼 스타일 */
.registration-form { text-align: center; padding: 20px 0; }
.form-desc { color: #666; margin-bottom: 40px; }
.select-group { display: flex; gap: 10px; margin-bottom: 30px; }
.luck-select { flex: 1; padding: 15px; border: 1px solid #eee; border-radius: 12px; font-size: 16px; }
.action-btn { width: 100%; padding: 18px; background: #00a651; color: white; border: none; border-radius: 12px; font-weight: 700; cursor: pointer; }
.action-btn:disabled { background: #ccc; }

/* 게이지 및 리포트 스타일 (이전과 동일하게 유지하되 간격 보정) */
.gauge-section { 
  position: relative; 
  /* 원 크기(180px)보다 넓게 설정하여 summary가 옆으로 퍼질 공간 확보 */
  width: 100%; 
  max-width: 450px; 
  margin: 40px auto 60px; 
  text-align: center; 
}

/* 실제 원형 SVG 크기는 고정 */
.gauge-svg { 
  width: 180px;
  height: 180px;
  transform: rotate(-90deg); 
}

.gauge-svg circle { fill: none; stroke-width: 8; stroke-linecap: round; }
.gauge-svg .bg { stroke: #f0fdf4; }
.gauge-svg .meter { stroke: #00a651; transition: stroke-dashoffset 1.5s ease-out; }

/* 점수 텍스트 위치 보정 (원 안의 정중앙) */
.gauge-text { 
  position: absolute; 
  top: 90px; /* 원 높이 180px의 절반 */
  left: 50%; 
  transform: translate(-45%, -45%); 
  text-align: center;
}

.score { font-size: 36px; font-weight: 900; color: #00a651; }

/* 요약 텍스트 수정 */
.summary { 
  margin-top: 30px; 
  color: #333; 
  font-size: 18px;    /* 가독성을 위해 살짝 키움 */
  line-height: 1.6; 
  font-weight: 700; 
  
  /* 너비 확장 및 줄바꿈 설정 */
  width: 100%;
  max-width: 380px;   /* 이 값을 조절해서 두 줄 라인을 맞추세요 */
  margin-left: auto;
  margin-right: auto;
  word-break: keep-all; /* 단어 단위 줄바꿈으로 깔끔하게 */
  text-align: center;
}
.report-list { border-top: 1.5px solid #f0f0f0; }
.report-item { border-bottom: 1px solid #f0f0f0; }
.report-header { width: 100%; padding: 25px 10px; display: flex; justify-content: space-between; background: none; border: none; cursor: pointer; }
.header-title { font-size: 18px; font-weight: 700; color: #333; }
.long-text { line-height: 2.2; color: #444; font-size: 15.5px; white-space: pre-line; padding: 0 10px 30px; }
.guide-box { background: #f9fdfa; padding: 20px; border-radius: 12px; color: #00a651; font-weight: 800; text-align: center; margin-bottom: 30px; }

.retry-btn { width: 100%; margin-top: 40px; padding: 15px; background: #f8faf9; border: 1px solid #e8f5e9; border-radius: 12px; color: #999; cursor: pointer; }
</style>