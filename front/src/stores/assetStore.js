import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from '@/api/index.js'

export const useAssetStore = defineStore('asset', () => {
  const assets = ref([])
  const categories = ref([])
  const financialInfo = ref({ income: 0, expense: 0 })

  // [Actions] 데이터 로드
  const getAssets = async () => {
    try {
      const response = await axios.get('/api/v1/assets/my-assets/')
      assets.value = response.data.sort((a, b) => {
        return (a.order || 0) - (b.order || 0)
      })
      return 'SUCCESS'
    } catch (error) {
      if (error.response && error.response.status === 401) return 'AUTH_ERROR'
      return 'API_ERROR'
    }
  }

  const getCategories = async () => {
    try {
      const response = await axios.get('/api/v1/assets/categories/')
      categories.value = response.data
    } catch (error) {
      console.error('카테고리 로드 실패', error)
    }
  }

  // API 호출 함수들 (기존 유지)
  const addAsset = async (payload) => axios.post('/api/v1/assets/my-assets/', payload)
  const updateAsset = async (id, payload) => axios.put(`/api/v1/assets/my-assets/${id}/`, payload)
  const deleteAsset = async (assetId) => axios.delete(`/api/v1/assets/my-assets/${assetId}/`)
  
  const getFinancialInfo = async () => {
    try {
      const response = await axios.get('/api/v1/assets/financial-info/')
      if (response.data) {
        financialInfo.value = {
            income: Number(response.data.monthly_income) || 0,
            expense: Number(response.data.monthly_expense) || 0
        }
      }
    } catch (error) { console.error(error) }
  }
  
  const saveFinancialInfo = async (payload) => {
    await axios.put('/api/v1/assets/financial-info/', payload)
  }

  // ---------------------------------------------------------
  // [Getters] 핵심 계산 로직 (순자산, 그룹별 분리)
  // ---------------------------------------------------------
  
  // 1. 카테고리 그룹 매핑 헬퍼
  const getGroup = (categoryId) => {
    const cat = categories.value.find(c => c.id === categoryId)
    return cat ? cat.group : null // 'CASH', 'INVEST', 'DEBT'
  }

  // 2. 그룹별 자산 리스트 분리
  const cashAssets = computed(() => assets.value.filter(a => getGroup(a.category) === 'CASH'))
  const investAssets = computed(() => assets.value.filter(a => getGroup(a.category) === 'INVEST'))
  const debtAssets = computed(() => assets.value.filter(a => getGroup(a.category) === 'DEBT'))

  // 3. 그룹별 총액 계산
  const totalCash = computed(() => cashAssets.value.reduce((sum, a) => sum + Number(a.current_value), 0))
  const totalInvest = computed(() => investAssets.value.reduce((sum, a) => sum + Number(a.current_value), 0))
  const totalDebt = computed(() => debtAssets.value.reduce((sum, a) => sum + Number(a.current_value), 0))

  // 4. 총 자산 (부채 제외, 현금+투자만)
  const totalAssets = computed(() => totalCash.value + totalInvest.value)

  // 5. 순자산 (총 자산 - 부채)
  const netWorth = computed(() => totalAssets.value - totalDebt.value)

  // 데이터 유무 확인
  const isDataExists = computed(() => assets.value.length > 0)

  return { 
    assets, categories, financialInfo, isDataExists,
    getAssets, getCategories, addAsset, updateAsset, deleteAsset, getFinancialInfo, saveFinancialInfo,
    // 추가된 Getters export
    cashAssets, investAssets, debtAssets,
    totalCash, totalInvest, totalDebt, totalAssets, netWorth
  }
})