import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const API_URL = 'http://127.0.0.1:8000'

  const token = ref(localStorage.getItem('token'))
  const nickname = ref(localStorage.getItem('nickname'))

  // 회원가압
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
          router.push({ name: 'assets' }) 
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


  // 로그인
  const logIn = function (payload) {
    return axios({
      method: 'post',
      url: `${API_URL}/api/accounts/login/`,
      data: payload
    })
      .then((res) => {
        const newToken = res.data.key || res.data.token
        const newNickname = res.data.user.nickname
        token.value = newToken
        nickname.value = newNickname
        localStorage.setItem('token', newToken)
        localStorage.setItem('nickname', newNickname)
        console.log('로그인 성공!')
      })
  }

  const logOut = function () {
    token.value = null
    nickname.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('nickname')
  }

  return { API_URL, token, signUp, nickname, logIn, logOut }
})