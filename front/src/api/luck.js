import axios from './index'

export const getLuckFortune = async () => {
  try {
    const response = await axios.post('/api/ais/luck/')
    return response.data
  } catch (error) {
    console.error('금전운 API 통신 에러:', error)
    throw error
  }
}