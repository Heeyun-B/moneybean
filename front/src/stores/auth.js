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

  return { API_URL, token, userNickname, signUp }
})