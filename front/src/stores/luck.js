import { ref } from 'vue'
import { defineStore } from 'pinia'
import { getLuckFortune } from '@/api/luck'

export const useLuckStore = defineStore('luck', () => {
  const luckResult = ref(null)
  const isLoading = ref(false)

  const fetchLuck = async (birthdate) => {
    isLoading.value = true
    try {
      const data = await getLuckFortune(birthdate)
      luckResult.value = data.fortune // 백엔드에서 주는 필드명에 맞춰 수정 필요
      return data
    } catch (error) {
      alert('금전운을 불러오는데 실패했습니다.')
      throw error
    } finally {
      isLoading.value = false
    }
  }

  return { luckResult, isLoading, fetchLuck }
})