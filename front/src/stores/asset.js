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
  const getAiDiagnosis = async (diagnosisData) => {
    try {
      const headers = getHeaders()

      const response = await axios.post(
        `${API_URL}/api/ais/diagnosis/`,
        diagnosisData,
        { headers }
      )

      // 백엔드에서 sections 배열 반환
      return response.data.sections  // 변경: response.data.report → response.data.sections

    } catch (error) {
      console.error("AI 진단 실패:", error)
      throw error
    }
  }

  // 5. [AI] 상품 추천 요청 Action
  const getAiRecommendations = async (diagnosisData) => {
    try {
      const headers = getHeaders()

      const response = await axios.post(
        `${API_URL}/api/ais/recommend/`,
        diagnosisData,
        { headers }
      )

      // 백엔드에서 success, data 형태로 반환
      return response.data

    } catch (error) {
      console.error("AI 상품 추천 실패:", error)
      return { success: false, message: error.message }
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
    getAiDiagnosis, getAiRecommendations
  }
})