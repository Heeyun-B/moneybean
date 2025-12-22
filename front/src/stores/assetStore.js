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
      // 순서(order) 기준 정렬
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

  // API 호출 함수들
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
  // [Getters] 핵심 계산 로직
  // ---------------------------------------------------------
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

  // ---------------------------------------------------------
  // [NEW] AI 진단 요청 액션 (Mocking)
  // ---------------------------------------------------------
  const getAiDiagnosis = async () => {
    try {
      // 1. 프롬프트에 넣을 데이터 구성
      const payload = {
        financialInfo: financialInfo.value,
        totalAssets: totalAssets.value,
        totalDebt: totalDebt.value,
        netWorth: netWorth.value,
        // AI가 이해하기 쉽게 필요한 필드만 추출
        cashList: cashAssets.value.map(a => ({ name: a.name, amount: a.current_value })),
        investList: investAssets.value.map(a => ({ name: a.name, category: a.category_name, amount: a.current_value })),
        debtList: debtAssets.value.map(a => ({ name: a.name, amount: a.current_value }))
      }

      console.log("🤖 [Mock] 백엔드로 전송할 데이터:", payload)

      // -----------------------------------------------------------
      // [TODO: to.백엔드, 여기를 실제 API 호출로 바꿔주세요!]
      // const response = await axios.post('/api/v1/assets/ai-diagnosis/', payload)
      // return response.data.report 
      // -----------------------------------------------------------

      // 3초 딜레이 (로딩 UI 테스트용)
      await new Promise(resolve => setTimeout(resolve, 3000))

      // 가짜 응답 반환
      return `
# 🌱 머니빈 AI 자산 진단 결과

## 📊 요약
현재 **순자산 ${netWorth.value.toLocaleString()}원**을 보유하고 계시네요! 
전체적으로 **안정적인 현금 흐름**을 가지고 계시지만, 부채 비율 관리가 필요해 보입니다.

## 💡 주요 발견
1. **현금 비중**: 비상금 확보가 잘 되어 있습니다.
2. **부채 관리**: 자산 대비 부채 비율을 조금 더 낮추는 것을 권장합니다.
3. **투자 성향**: 현재 포트폴리오 구성을 보았을 때 안정 지향적으로 보입니다.

## 🚀 추천 액션
- **고금리 부채**가 있다면 최우선으로 상환하세요.
- **분산 투자**를 통해 리스크를 줄여보세요.

*이 진단은 참고용이며, 투자의 책임은 본인에게 있습니다.*
      `
    } catch (error) {
      console.error("AI 진단 실패:", error)
      throw error
    }
  }

  return { 
    assets, categories, financialInfo, isDataExists,
    getAssets, getCategories, addAsset, updateAsset, deleteAsset, getFinancialInfo, saveFinancialInfo,
    cashAssets, investAssets, debtAssets,
    totalCash, totalInvest, totalDebt, totalAssets, netWorth,
    getAiDiagnosis // [NEW] 추가됨
  }
})