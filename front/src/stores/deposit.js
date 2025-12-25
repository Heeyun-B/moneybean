import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useDepositStore = defineStore('deposit', () => {
  const authStore = useAuthStore()
  const API_URL = 'http://127.0.0.1:8000/api/deposits' 

  // --- State ---
  const depositProducts = ref([])
  const depositDetail = ref(null)
  
  const savingProducts = ref([])
  const savingDetail = ref(null)

  const mySubscriptions = ref([]) 
  const mySavingSubscriptions = ref([]) 

  // --- Actions ---

  // [예금] 목록 조회
  const getDepositProducts = function (bankName = '') {
    const config = {
      method: 'get',
      url: `${API_URL}/deposit-products/`,
      params: bankName ? { bank: bankName } : {}
    }

    // 로그인 상태일 때만 Authorization 헤더 추가
    if (authStore.token) {
      config.headers = { Authorization: `Token ${authStore.token}` }
    }

    return axios(config)
      .then((res) => {
        depositProducts.value = res.data
        return res.data
      })
      .catch((err) => {
        console.error('예금 목록 로드 실패:', err.response?.data || err.message)
        depositProducts.value = []
        throw err
      })
  }

  // [예금] DB 저장 (Scraping)
  const saveDepositProducts = function () {
    const config = {
      method: 'post',
      url: `${API_URL}/save-deposit-products/`
    }

    // 로그인 상태일 때만 Authorization 헤더 추가
    if (authStore.token) {
      config.headers = { Authorization: `Token ${authStore.token}` }
    }

    return axios(config)
  }

  // [적금] 목록 조회
  const getSavingProducts = function () {
    const config = {
      method: 'get',
      url: `${API_URL}/saving-products/`
    }

    // 로그인 상태일 때만 Authorization 헤더 추가
    if (authStore.token) {
      config.headers = { Authorization: `Token ${authStore.token}` }
    }

    return axios(config)
      .then((res) => {
        savingProducts.value = res.data
        return res.data
      })
      .catch((err) => {
        console.error('적금 목록 로드 실패:', err.response?.data || err.message)
        savingProducts.value = []
        throw err
      })
  }

  // [적금] DB 저장 (Scraping)
  const saveSavingProducts = function () {
    const config = {
      method: 'post',
      url: `${API_URL}/save-saving-products/`
    }

    // 로그인 상태일 때만 Authorization 헤더 추가
    if (authStore.token) {
      config.headers = { Authorization: `Token ${authStore.token}` }
    }

    return axios(config)
  }

  // [예금] 상세 조회
  const getDepositDetail = function (finPrdtCd) {
    const config = {
      method: 'get',
      url: `${API_URL}/deposit-products/${finPrdtCd}/`
    }

    // 로그인 상태일 때만 Authorization 헤더 추가
    if (authStore.token) {
      config.headers = { Authorization: `Token ${authStore.token}` }
    }

    return axios(config)
      .then((res) => depositDetail.value = res.data)
      .catch((err) => console.log(err))
  }

  // [적금] 상세 조회
  const getSavingDetail = function (finPrdtCd) {
    const config = {
      method: 'get',
      url: `${API_URL}/saving-products/${finPrdtCd}/`
    }

    // 로그인 상태일 때만 Authorization 헤더 추가
    if (authStore.token) {
      config.headers = { Authorization: `Token ${authStore.token}` }
    }

    return axios(config)
      .then((res) => savingDetail.value = res.data)
      .catch((err) => console.log('적금 상세 로드 실패:', err))
  }

  // [예금] 가입하기
  const subscribeProduct = function (finPrdtCd, optionId) {
    return axios({
      method: 'post',
      url: `${API_URL}/deposit-products/${finPrdtCd}/subscribe/`,
      data: { selected_option: optionId },
      headers: { Authorization: `Token ${authStore.token}` }
    })
  }

  // [적금] 가입하기
  const subscribeSaving = function (finPrdtCd, optionId) {
    return axios({
      method: 'post',
      url: `${API_URL}/saving-products/${finPrdtCd}/subscribe/`,
      data: { selected_option: optionId },
      headers: { Authorization: `Token ${authStore.token}` }
    })
  }

  // [예금] 가입 해제
  const unsubscribeProduct = function (finPrdtCd) {
    return axios({
      method: 'delete',
      url: `${API_URL}/deposit-products/${finPrdtCd}/unsubscribe/`,
      headers: { Authorization: `Token ${authStore.token}` }
    })
  }

  // [적금] 가입 해제
  const unsubscribeSaving = function (finPrdtCd) {
    return axios({
      method: 'delete',
      url: `${API_URL}/saving-products/${finPrdtCd}/unsubscribe/`,
      headers: { Authorization: `Token ${authStore.token}` }
    })
  }

  // [예금] 내 가입 목록
  const getMySubscriptions = function () {
    return axios({
      method: 'get',
      url: `${API_URL}/my-subscriptions-deposit/`,
      headers: { Authorization: `Token ${authStore.token}` }
    })
      .then((res) => mySubscriptions.value = res.data)
      .catch((err) => console.log('예금 가입 목록 로드 실패:', err))
  }

  // [적금] 내 가입 목록
  const getMySavingSubscriptions = function () {
    return axios({
      method: 'get',
      url: `${API_URL}/my-subscriptions-saving/`,
      headers: { Authorization: `Token ${authStore.token}` }
    })
      .then((res) => mySavingSubscriptions.value = res.data)
      .catch((err) => console.log('적금 가입 목록 로드 실패:', err))
  }

  return { 
    depositProducts, depositDetail, 
    savingProducts, savingDetail,
    mySubscriptions, mySavingSubscriptions,
    getDepositProducts, getSavingProducts,
    saveDepositProducts, saveSavingProducts,
    getDepositDetail, getSavingDetail,
    subscribeProduct, subscribeSaving,
    unsubscribeProduct, unsubscribeSaving,
    getMySubscriptions, getMySavingSubscriptions
  }
})