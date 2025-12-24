/**
 * 언론사 코드를 한글 이름으로 매핑
 */
export const PRESS_NAME_MAP = {
  'pinpointnews': '핀포인트뉴스',
  'ggilbo': '금강일보',
  'biztribune': '비즈트리뷴',
  'techm': 'TechM',
  'tbc': 'TBC뉴스',
  '언론사658': '국제신문',
  'lcnews': '라이센스뉴스',
  'efnews': '파이낸셜신문',
  'segyebiz': '세계비즈',
  'm-i': '매일일보',
}

/**
 * 언론사 코드를 한글 이름으로 변환
 * @param {string} pressCode - 언론사 코드
 * @returns {string} 한글 이름 또는 원본 코드
 */
export const getPressDisplayName = (pressCode) => {
  if (!pressCode) return '언론사'
  return PRESS_NAME_MAP[pressCode] || pressCode
}
