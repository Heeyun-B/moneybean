import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const API_URL = 'http://127.0.0.1:8000'

  const token = ref(localStorage.getItem('token'))

  const signUp = function (payload) {
    axios({
      method: 'post',
      url: `${API_URL}/api/accounts/signup/`, 
      data: payload
    })
      .then((res) => {
        const newToken = res.data.token
        token.value = newToken
        localStorage.setItem('token', newToken)

        const userResponse = window.confirm('가입을 환영합니다!\n바로 "내 자산"을 입력하시겠습니까?')

        if (userResponse) {
          router.push({ name: 'asset' }) 
        } else {
          router.push({ name: 'home' })
        }
      })
      .catch((err) => {
        console.log(err)
        const msg = err.response?.data ? JSON.stringify(err.response.data) : '입력을 확인해주세요.'
        window.alert(`회원가입 실패!\n${msg}`)
      })
  }

  return { API_URL, token, signUp }
})