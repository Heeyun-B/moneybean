import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(localStorage.getItem('token'))
  const userNickname = ref(localStorage.getItem('nickname'))

  // 1. Getters (로그인 상태 확인용)
  const isAuthenticated = computed(() => !!token.value)

  // 2. Actions
  const signUp = async function (payload) {
    try {
      const res = await axios.post(`${API_URL}/api/accounts/signup/`, payload)
      return res.data
    } catch (err) {
      console.error('회원가입 에러:', err)
      throw err 
    }
  }

  const logIn = async function (payload) {
    try {
      const res = await axios.post(`${API_URL}/api/accounts/login/`, payload)
      
      const newToken = res.data.key || res.data.token
      const newNickname = res.data.user?.nickname || res.data.nickname || '사용자'

      if (newToken) {
        setToken(newToken, newNickname)
      } else {
        throw new Error("토큰을 받아오지 못했습니다.")
      }
      return res.data
    } catch (err) {
      console.error('로그인 에러:', err)
      throw err
    }
  }

  const logOut = function () {
    token.value = null
    userNickname.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('nickname')
  }

  // 내부 헬퍼 함수
  const setToken = (newToken, newNickname) => {
    token.value = newToken
    userNickname.value = newNickname
    localStorage.setItem('token', newToken)
    localStorage.setItem('nickname', newNickname)
  }

  return { 
    API_URL, 
    token, 
    userNickname, 
    isAuthenticated,
    signUp, 
    logIn, 
    logOut 
  }
})