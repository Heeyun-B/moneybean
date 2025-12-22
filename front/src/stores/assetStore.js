import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAssetStore = defineStore('asset', () => {
  const assets = ref([])
  
  // ... (getters 생략)

  const getAssets = async () => {
    // 1. 토큰이 아예 없는 경우 체크
    const token = localStorage.getItem('token')
    if (!token) {
      console.log('토큰이 없습니다.')
      return 'NO_TOKEN' // 토큰 없음 신호 반환
    }

    try {
      const response = await axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/assets/my-assets/',
        headers: {
          Authorization: `Token ${token}`
        }
      })
      assets.value = response.data
      return 'SUCCESS' // 성공 신호 반환

    } catch (error) {
      console.error('자산 정보 불러오기 실패:', error)
      // 2. 토큰이 만료되었거나 유효하지 않은 경우 (401 에러)
      if (error.response && error.response.status === 401) {
        return 'AUTH_ERROR' // 인증 실패 신호 반환
      }
      return 'API_ERROR' // 기타 에러
    }
  }

  return { assets, isDataExists, totalValue, getAssets }
})