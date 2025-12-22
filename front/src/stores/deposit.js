import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useDepositStore = defineStore('deposit', () => {
  const authStore = useAuthStore()
  const depositProducts = ref([])
  const depositDetail = ref(null)
  const mySubscriptions = ref([])
  const API_URL = 'http://127.0.0.1:8000/api/deposits'

  // 1. 전체 정기예금 목록 가져오기
  const getDepositProducts = function (bankName = '') {
    axios({
      method: 'get',
      url: `${API_URL}/deposit-products/`,
      params: {
        bank: bankName
      },
      headers: {
        Authorization: authStore.token ? `Token ${authStore.token}` : ''
      }
    })
      .then((res) => {
        depositProducts.value = res.data
      })
      .catch((err) => {
        console.log('상품 로드 실패:', err)
        if (err.response?.status === 401) {
          console.log('인증 실패: 토큰이 없거나 만료되었습니다.')
        }
      })
  }

  // 2. 특정 상품 상세 정보 가져오기
  const getDepositDetail = function (finPrdtCd) {
    axios({
      method: 'get',
      url: `${API_URL}/deposit-products/${finPrdtCd}/`,
      headers: {
        Authorization: authStore.token ? `Token ${authStore.token}` : ''
      }
    })
      .then((res) => {
        depositDetail.value = res.data
      })
      .catch((err) => console.log('상세정보 로드 실패:', err))
  }

  // 3. 상품 가입하기
  const subscribeProduct = function (finPrdtCd, optionId, token) {
    return axios({
      method: 'post',
      url: `${API_URL}/deposit-products/${finPrdtCd}/subscribe/`,
      data: {
        selected_option: optionId
      },
      headers: {
        Authorization: `Token ${token}`
      }
    })
  }

  // 4. 가입 취소하기
  const unsubscribeProduct = function (finPrdtCd, token) {
    return axios({
      method: 'delete',
      url: `${API_URL}/deposit-products/${finPrdtCd}/unsubscribe/`,
      headers: {
        Authorization: `Token ${token}`
      }
    })
  }

  return { 
    depositProducts, 
    depositDetail, 
    mySubscriptions,
    getDepositProducts, 
    getDepositDetail,
    subscribeProduct,
    unsubscribeProduct
  }
})