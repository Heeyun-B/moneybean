import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(localStorage.getItem('token'))
  const userNickname = ref(localStorage.getItem('nickname'))

  const signUp = async function (payload) {
    try {
      const res = await axios({
        method: 'post',
        url: `${API_URL}/api/accounts/signup/`, 
        data: payload
      })
      
      const newToken = res.data.token || res.data.key
      
      if (newToken) {
        token.value = newToken
        localStorage.setItem('token', newToken)
        
        if (res.data.user || res.data.nickname) {
           const nickname = res.data.user?.nickname || res.data.nickname || payload.nickname
           userNickname.value = nickname
           localStorage.setItem('nickname', nickname)
        }
      }
      
      return res
    } catch (err) {
      console.error(err)
      throw err 
    }
  }


  // 로그인
  const logIn = function (payload) {
  return axios({
    method: 'post',
    url: `${API_URL}/api/accounts/login/`,
    data: payload
  })
    .then((res) => {
      const newToken = res.data.key || res.data.token
      const newNickname = res.data.user?.nickname || res.data.nickname || '사용자'

      token.value = newToken
      nickname.value = newNickname
      
      localStorage.setItem('token', newToken)
      localStorage.setItem('nickname', newNickname)
      
      console.log('로그인 성공! 닉네임:', newNickname)
    })
    .catch((err) => {
      console.error('로그인 실패 사유:', err.response?.data)
      throw err
    })
}
  // 로그아웃
  const logOut = function () {
    token.value = null
    nickname.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('nickname')
  }

  return { API_URL, token, signUp, nickname, logIn, logOut }
})