import axios from '@/api/index'

/**
 * 금융 뉴스 API 서비스
 */

/**
 * 뉴스 목록 조회
 * @returns {Promise} 뉴스 목록
 */
export const getNewsList = async () => {
  try {
    const response = await axios.get('/api/finance_news/news/')
    return response.data
  } catch (error) {
    console.error('뉴스 목록 조회 실패:', error)
    throw error
  }
}

/**
 * 뉴스 상세 조회
 * @param {number} newsId - 뉴스 ID
 * @returns {Promise} 뉴스 상세 정보
 */
export const getNewsDetail = async (newsId) => {
  try {
    const response = await axios.get(`/api/finance_news/news/${newsId}/`)
    return response.data
  } catch (error) {
    console.error('뉴스 상세 조회 실패:', error)
    throw error
  }
}

/**
 * 뉴스 크롤링 (관리자 전용)
 * @param {string} query - 검색 키워드 (기본값: '금융')
 * @returns {Promise} 크롤링 결과
 */
export const crawlNews = async (query = '금융') => {
  try {
    const response = await axios.post('/api/finance_news/news/crawl/', { query })
    return response.data
  } catch (error) {
    console.error('뉴스 크롤링 실패:', error)
    throw error
  }
}
