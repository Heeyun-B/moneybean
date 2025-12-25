import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useBoardStore } from './board' // 추가

export const useAuthStore = defineStore('auth', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const storageImg = localStorage.getItem('profileImage')
  const profileImage = ref(storageImg && storageImg !== 'null' ? storageImg : null)
  const token = ref(localStorage.getItem('token'))
  const userNickname = ref(localStorage.getItem('nickname'))
  const userRole = ref(localStorage.getItem('userRole') || 'user')
  const isStaff = ref(localStorage.getItem('isStaff') === 'true')

  const isAuthenticated = computed(() => !!token.value)

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
      const newNickname = res.data.user?.nickname || '사용자'
      const newRole = res.data.user?.role || res.data.role || 'user'
      const newIsStaff = res.data.user?.is_staff || false
      const newProfileImg = res.data.user?.profile_image_url || res.data.user?.profile_image || null

      if (newToken) {
        setToken(newToken, newNickname, newRole, newIsStaff, newProfileImg)
      }
      return res.data
    } catch (err) {
      console.error('로그인 에러:', err); throw err
    }
  }

  const logOut = function () {
    token.value = null
    userNickname.value = null
    userRole.value = 'user'
    isStaff.value = false
    profileImage.value = null
    
    localStorage.removeItem('token')
    localStorage.removeItem('nickname')
    localStorage.removeItem('userRole')
    localStorage.removeItem('isStaff')
    localStorage.removeItem('profileImage')

    // 게시판 스토어 초기화 (추가)
    const boardStore = useBoardStore()
    boardStore.likedPosts = []
  }

  const setToken = (newToken, newNickname, newRole = 'user', newIsStaff = false, newProfileImg) => {
    token.value = newToken
    userNickname.value = newNickname
    userRole.value = newRole
    isStaff.value = newIsStaff
    
    let imgUrl = newProfileImg
    if (imgUrl && !imgUrl.startsWith('http')) {
      imgUrl = `${API_URL}${imgUrl}`
    }
    
    profileImage.value = imgUrl
    
    localStorage.setItem('token', newToken)
    localStorage.setItem('nickname', newNickname)
    localStorage.setItem('userRole', newRole)
    localStorage.setItem('isStaff', newIsStaff.toString())
    localStorage.setItem('profileImage', imgUrl || '')
  }

  const updateUserInfo = (userData) => {
    if (userData.nickname) {
      userNickname.value = userData.nickname
      localStorage.setItem('nickname', userData.nickname)
    }
    
    const newImg = userData.profile_image_url || userData.profile_image
    if (newImg) {
      let imgUrl = newImg
      if (!imgUrl.startsWith('http')) {
        imgUrl = `${API_URL}${imgUrl}`
      }
      profileImage.value = imgUrl
      localStorage.setItem('profileImage', imgUrl)
    }
  }

  return {
    API_URL, token, userNickname, userRole, isStaff,
    isAuthenticated, signUp, logIn, logOut, updateUserInfo, profileImage
  }
})