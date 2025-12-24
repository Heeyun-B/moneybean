import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(localStorage.getItem('token'))
  const userNickname = ref(localStorage.getItem('nickname'))
  const userRole = ref(localStorage.getItem('userRole') || 'user')
  const isStaff = ref(localStorage.getItem('isStaff') === 'true')

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

      const newToken = res.data.token || res.data.key
      const newNickname = res.data.user?.nickname || res.data.nickname || '사용자'
      const newRole = res.data.user?.role || res.data.role || 'user'
      const newIsStaff = res.data.user?.is_staff || false

      console.log('로그인 응답:', res.data)
      console.log('is_staff 값:', newIsStaff)

      if (newToken) {
        setToken(newToken, newNickname, newRole, newIsStaff)
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
    userRole.value = 'user'
    isStaff.value = false
    localStorage.removeItem('token')
    localStorage.removeItem('nickname')
    localStorage.removeItem('userRole')
    localStorage.removeItem('isStaff')
  }

  // 내부 헬퍼 함수
  const setToken = (newToken, newNickname, newRole = 'user', newIsStaff = false) => {
    token.value = newToken
    userNickname.value = newNickname
    userRole.value = newRole
    isStaff.value = newIsStaff
    localStorage.setItem('token', newToken)
    localStorage.setItem('nickname', newNickname)
    localStorage.setItem('userRole', newRole)
    localStorage.setItem('isStaff', newIsStaff.toString())
  }

  return {
    API_URL,
    token,
    userNickname,
    userRole,
    isStaff,
    isAuthenticated,
    signUp,
    logIn,
    logOut
  }
})