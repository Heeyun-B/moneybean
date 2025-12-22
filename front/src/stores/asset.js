import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth' // 토큰 사용을 위해 Auth 스토어 연결 권장

export const useAssetStore = defineStore('asset', () => {
  const authStore = useAuthStore()
  const API_URL = 'http://127.0.0.1:8000' // 실제 백엔드 주소로 변경 필요

  const assets = ref([])
  const categories = ref([])
  const financialInfo = ref({ income: 0, expense: 0 })

  // 1. 공통 헤더 설정 (토큰 포함)
  const getHeaders = () => {
    const token = localStorage.getItem('token')
    return token ? { Authorization: `Token ${token}` } : {}
  }

  // 2. 데이터 로드 Actions
  const getAssets = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/assets/my-assets/`, { headers: getHeaders() })
      // 순서(order) 기준 정렬
      assets.value = response.data.sort((a, b) => (a.order || 0) - (b.order || 0))
      return 'SUCCESS'
    } catch (error) {
      if (error.response && error.response.status === 401) return 'AUTH_ERROR'
      console.error('자산 로드 실패:', error)
      return 'API_ERROR'
    }
  }

  const getCategories = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/assets/categories/`, { headers: getHeaders() })
      categories.value = response.data
    } catch (error) {
      console.error('카테고리 로드 실패', error)
    }
  }

  const getFinancialInfo = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/assets/financial-info/`, { headers: getHeaders() })
      if (response.data) {
        financialInfo.value = {
          income: Number(response.data.monthly_income) || 0,
          expense: Number(response.data.monthly_expense) || 0
        }
      }
    } catch (error) {
      console.error('재정 정보 로드 실패', error)
    }
  }

  // 3. CRUD Actions
  const addAsset = async (payload) => axios.post(`${API_URL}/api/v1/assets/my-assets/`, payload, { headers: getHeaders() })
  const updateAsset = async (id, payload) => axios.put(`${API_URL}/api/v1/assets/my-assets/${id}/`, payload, { headers: getHeaders() })
  const deleteAsset = async (assetId) => axios.delete(`${API_URL}/api/v1/assets/my-assets/${assetId}/`, { headers: getHeaders() })
  
  const saveFinancialInfo = async (payload) => {
    await axios.put(`${API_URL}/api/v1/assets/financial-info/`, payload, { headers: getHeaders() })
  }

  // 4. [AI] 진단 요청 Action
  const getAiDiagnosis = async () => {
    try {
      // 백엔드 전송용 페이로드 구성
      const payload = {
        financialInfo: financialInfo.value,
        totalAssets: totalAssets.value,
        totalDebt: totalDebt.value,
        netWorth: netWorth.value,
        // 상세 자산 리스트 포함 (분석 정확도 향상)
        assets: assets.value.map(a => ({ 
           name: a.name, 
           amount: a.current_value, 
           category: a.category 
        }))
      }

      console.log("🤖 [AI Request Payload]:", payload)

      // [TODO: Backend 연동 시 아래 주석 해제 및 Mocking 제거]
      // const response = await axios.post(`${API_URL}/api/v1/assets/ai-diagnosis/`, payload, { headers: getHeaders() })
      // return response.data.report 

      // --- Mocking Start (테스트용 가짜 응답) ---
      await new Promise(resolve => setTimeout(resolve, 3000)) // 3초 대기
      
      return `
# 🤖 머니빈 AI 분석 리포트

## 📊 자산 포트폴리오 진단
회원님의 총 자산은 **${totalAssets.value.toLocaleString()}원**이며, 
순자산은 **${netWorth.value.toLocaleString()}원** 입니다.

## 💡 맞춤형 조언
1. **유동성 관리**: 현금성 자산 비중이 **${((totalCash.value / totalAssets.value) * 100).toFixed(1)}%**로 적절합니다.
2. **부채 관리**: 부채 비율이 다소 높다면 고금리 대출부터 상환 계획을 세워보세요.
3. **투자 제안**: 포트폴리오 다각화를 통해 리스크를 관리하세요.

*이 기능은 현재 테스트 모드입니다.*
      `
      // --- Mocking End ---

    } catch (error) {
      console.error("AI 진단 실패:", error)
      throw error
    }
  }

  // 5. Getters (계산 로직)
  const getGroup = (categoryId) => {
    const cat = categories.value.find(c => c.id === categoryId)
    return cat ? cat.group : null 
  }

  const cashAssets = computed(() => assets.value.filter(a => getGroup(a.category) === 'CASH'))
  const investAssets = computed(() => assets.value.filter(a => getGroup(a.category) === 'INVEST'))
  const debtAssets = computed(() => assets.value.filter(a => getGroup(a.category) === 'DEBT'))

  const totalCash = computed(() => cashAssets.value.reduce((sum, a) => sum + Number(a.current_value), 0))
  const totalInvest = computed(() => investAssets.value.reduce((sum, a) => sum + Number(a.current_value), 0))
  const totalDebt = computed(() => debtAssets.value.reduce((sum, a) => sum + Number(a.current_value), 0))

  const totalAssets = computed(() => totalCash.value + totalInvest.value)
  const netWorth = computed(() => totalAssets.value - totalDebt.value)
  const isDataExists = computed(() => assets.value.length > 0)

  return { 
    assets, categories, financialInfo, isDataExists,
    getAssets, getCategories, addAsset, updateAsset, deleteAsset, getFinancialInfo, saveFinancialInfo,
    cashAssets, investAssets, debtAssets,
    totalCash, totalInvest, totalDebt, totalAssets, netWorth,
    getAiDiagnosis
  }
})