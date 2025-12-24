import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'
import { getNewsList, getNewsDetail } from '@/api/news'
import { getPressDisplayName } from '@/utils/pressMapping'

export const useBoardStore = defineStore('board', () => {
  const authStore = useAuthStore()
  const API_URL = authStore.API_URL

  // 게시판별 게시글 목록
  const freePosts = ref([])
  const newsPosts = ref([])
  const infoPosts = ref([])

  // 댓글 목록
  const comments = ref({})

  // 좋아요한 게시글 목록 (postId 배열)
  const likedPosts = ref(JSON.parse(localStorage.getItem('likedPosts') || '[]'))

  // Getter: 게시판 타입에 따른 게시글 목록 반환
  const getPosts = (boardType) => {
    switch (boardType) {
      case 'free':
        return freePosts.value
      case 'news':
        return newsPosts.value
      case 'info':
        return infoPosts.value
      default:
        return []
    }
  }

  // Getter: 특정 게시글 가져오기
  const getPost = (boardType, postId) => {
    const posts = getPosts(boardType)
    return posts.find(post => post.id === parseInt(postId))
  }

  // Getter: 특정 게시글의 댓글 목록
  const getComments = (postId) => {
    return comments.value[postId] || []
  }

  // Getter: 게시글 좋아요 여부
  const isLiked = (postId) => {
    return likedPosts.value.includes(postId)
  }

  // Getter: 좋아요한 게시글 목록
  const getLikedPosts = () => {
    const freePostsWithType = freePosts.value.map(post => ({ ...post, boardType: 'free' }))
    const newsPostsWithType = newsPosts.value.map(post => ({ ...post, boardType: 'news' }))
    const infoPostsWithType = infoPosts.value.map(post => ({ ...post, boardType: 'info' }))

    const allPosts = [...freePostsWithType, ...newsPostsWithType, ...infoPostsWithType]
    return allPosts.filter(post => likedPosts.value.includes(post.id))
  }

  // Actions

  // 1. 게시글 목록 조회
  const fetchPosts = async (boardType) => {
    try {
      let apiPath = ''
      let response = null

      switch (boardType) {
        case 'free':
          apiPath = `${API_URL}/api/boards/`
          response = await axios.get(apiPath, {
            headers: authStore.token ? {
              Authorization: `Token ${authStore.token}`
            } : {}
          })
          break
        case 'info':
          apiPath = `${API_URL}/api/finance_infos/`
          response = await axios.get(apiPath, {
            headers: authStore.token ? {
              Authorization: `Token ${authStore.token}`
            } : {}
          })
          break
        case 'news':
          // 뉴스 API 호출
          try {
            const newsData = await getNewsList()
            const newsPosts_data = newsData.map(article => {
              const content = article.content || ''
              const pressDisplayName = getPressDisplayName(article.press)
              // 로컬에서 좋아요 개수 계산
              const likeCount = likedPosts.value.includes(article.id) ? 1 : 0
              return {
                id: article.id,
                title: article.title || '제목 없음',
                content: content,
                author: pressDisplayName,
                created_at: article.published_date || article.crawled_at,
                comment_count: 0,
                like_count: likeCount,
                is_notice: false,
                link: article.link,
                press: pressDisplayName,
                pressCode: article.press,
                content_preview: content.substring(0, 100) + (content.length > 100 ? '...' : '')
              }
            })
            newsPosts.value = newsPosts_data
            return newsPosts_data
          } catch (newsError) {
            console.error('뉴스 API 호출 실패:', newsError)
            console.error('에러 상세:', newsError.response?.data || newsError.message)
            // 에러 발생 시에도 빈 배열 반환하여 페이지가 깨지지 않도록 함
            newsPosts.value = []
            return []
          }
        default:
          throw new Error('Invalid board type')
      }

      const posts = response.data.map(post => ({
        id: post.id,
        title: post.title,
        content: post.content,
        author: post.username,
        created_at: post.created_at,
        comment_count: post.comment_count || 0,
        like_count: post.like_count || 0,
        is_notice: false,
        content_preview: post.content.substring(0, 100) + (post.content.length > 100 ? '...' : '')
      }))

      switch (boardType) {
        case 'free':
          freePosts.value = posts
          break
        case 'info':
          infoPosts.value = posts
          break
      }

      return posts
    } catch (error) {
      console.error('게시글 목록 조회 실패:', error)
      console.error('boardType:', boardType)
      console.error('에러 상세:', error.response?.data || error.message)

      // 목 데이터 사용 (뉴스 제외)
      const mockPosts = generateMockPosts(boardType)
      switch (boardType) {
        case 'free':
          freePosts.value = mockPosts
          break
        case 'info':
          infoPosts.value = mockPosts
          break
      }
      return mockPosts
    }
  }

  // 2. 게시글 상세 조회
  const fetchPostDetail = async (boardType, postId) => {
    try {
      let apiPath = ''
      let response = null
      let post = null

      switch (boardType) {
        case 'free':
          apiPath = `${API_URL}/api/boards/articles/${postId}/`
          response = await axios.get(apiPath, {
            headers: authStore.token ? {
              Authorization: `Token ${authStore.token}`
            } : {}
          })
          post = {
            id: response.data.id,
            title: response.data.title,
            content: response.data.content,
            author: response.data.username,
            created_at: response.data.created_at,
            updated_at: response.data.updated_at,
            comment_count: response.data.comment_count || 0,
            like_count: response.data.like_count || 0,
            is_liked: response.data.is_liked || false,
            is_notice: response.data.is_notice || false,
          }
          if (response.data.comments) {
            comments.value[postId] = response.data.comments.map(comment => ({
              id: comment.id,
              content: comment.content,
              author: comment.username,
              created_at: comment.created_at
            }))
          }
          break
        case 'info':
          apiPath = `${API_URL}/api/finance_infos/info/${postId}/`
          response = await axios.get(apiPath, {
            headers: authStore.token ? {
              Authorization: `Token ${authStore.token}`
            } : {}
          })
          post = {
            id: response.data.id,
            title: response.data.title,
            content: response.data.content,
            author: response.data.username,
            created_at: response.data.created_at,
            updated_at: response.data.updated_at,
            comment_count: response.data.comment_count || 0,
            like_count: response.data.like_count || 0,
            is_liked: response.data.is_liked || false,
            is_notice: response.data.is_notice || false,
          }
          if (response.data.comments) {
            comments.value[postId] = response.data.comments.map(comment => ({
              id: comment.id,
              content: comment.content,
              author: comment.username,
              created_at: comment.created_at
            }))
          }
          break
        case 'news':
          // 뉴스 상세 조회
          const newsDetail = await getNewsDetail(postId)
          const pressDisplayName = getPressDisplayName(newsDetail.press)
          // 로컬에서 좋아요 상태 확인
          const isNewsLiked = likedPosts.value.includes(parseInt(postId))
          const newsLikeCount = isNewsLiked ? 1 : 0
          post = {
            id: newsDetail.id,
            title: newsDetail.title,
            content: newsDetail.content,
            author: pressDisplayName,
            created_at: newsDetail.published_date || newsDetail.crawled_at,
            updated_at: newsDetail.published_date || newsDetail.crawled_at,
            comment_count: 0,
            like_count: newsLikeCount,
            is_liked: isNewsLiked,
            is_notice: false,
            link: newsDetail.link,
            press: pressDisplayName,
            pressCode: newsDetail.press,
          }
          break
        default:
          throw new Error('Invalid board type')
      }

      const posts = getPosts(boardType)
      const index = posts.findIndex(p => p.id === parseInt(postId))
      if (index !== -1) {
        posts[index] = { ...posts[index], ...post }
      } else {
        posts.push({
          ...post,
          content_preview: post.content.substring(0, 100) + (post.content.length > 100 ? '...' : '')
        })
      }

      return post
    } catch (error) {
      console.error('게시글 상세 조회 실패:', error)
      throw error
    }
  }

  // 3. 게시글 작성
  const createPost = async (boardType, postData) => {
    try {
      let apiPath = ''
      switch (boardType) {
        case 'free':
          apiPath = `${API_URL}/api/boards/`
          break
        case 'info':
          apiPath = `${API_URL}/api/finance_infos/`
          break
        case 'news':
          throw new Error('뉴스는 작성할 수 없습니다.')
        default:
          throw new Error('Invalid board type')
      }

      const response = await axios.post(
        apiPath,
        postData,
        {
          headers: {
            Authorization: `Token ${authStore.token}`
          }
        }
      )

      const newPost = {
        id: response.data.id,
        title: response.data.title,
        content: response.data.content,
        author: response.data.username,
        created_at: response.data.created_at,
        comment_count: 0,
        like_count: 0,
        is_notice: false,
        content_preview: response.data.content.substring(0, 100)
      }

      switch (boardType) {
        case 'free':
          freePosts.value.unshift(newPost)
          break
        case 'info':
          infoPosts.value.unshift(newPost)
          break
      }

      return response.data.id
    } catch (error) {
      console.error('게시글 작성 실패:', error)
      if (error.response?.status === 401 || error.response?.status === 403) {
        throw new Error(error.response?.data?.error || error.response?.data?.detail || '작성 권한이 없습니다.')
      }
      throw error
    }
  }

  // 4. 게시글 수정
  const updatePost = async (boardType, postId, postData) => {
    try {
      let apiPath = ''
      switch (boardType) {
        case 'free':
          apiPath = `${API_URL}/api/boards/articles/${postId}/`
          break
        case 'info':
          apiPath = `${API_URL}/api/finance_infos/info/${postId}/`
          break
        case 'news':
          throw new Error('뉴스는 수정할 수 없습니다.')
        default:
          throw new Error('Invalid board type')
      }

      const response = await axios.put(
        apiPath,
        postData,
        {
          headers: {
            Authorization: `Token ${authStore.token}`
          }
        }
      )

      const posts = getPosts(boardType)
      const index = posts.findIndex(p => p.id === parseInt(postId))
      if (index !== -1) {
        posts[index] = {
          ...posts[index], // 기존 정보 유지
          title: response.data.title,
          content: response.data.content,
          updated_at: response.data.updated_at,
          content_preview: response.data.content.substring(0, 100)
        }
      }

      return response.data
    } catch (error) {
      console.error('게시글 수정 실패:', error)
      throw error
    }
  }

  // 5. 게시글 삭제
  const deletePost = async (boardType, postId) => {
    try {
      let apiPath = ''
      switch (boardType) {
        case 'free':
          apiPath = `${API_URL}/api/boards/articles/${postId}/`
          break
        case 'info':
          apiPath = `${API_URL}/api/finance_infos/info/${postId}/`
          break
        case 'news':
          throw new Error('뉴스는 삭제할 수 없습니다.')
        default:
          throw new Error('Invalid board type')
      }

      await axios.delete(apiPath, {
        headers: {
          Authorization: `Token ${authStore.token}`
        }
      })

      const posts = getPosts(boardType)
      const index = posts.findIndex(p => p.id === parseInt(postId))
      if (index !== -1) {
        posts.splice(index, 1)
      }
    } catch (error) {
      console.error('게시글 삭제 실패:', error)
      throw error
    }
  }

  // 6. 댓글 목록 조회
  const fetchComments = async (postId) => {
    if (comments.value[postId]) return comments.value[postId]
    if (!comments.value[postId]) comments.value[postId] = []
    return comments.value[postId]
  }

  // 7. 댓글 작성
  const createComment = async (boardType, postId, commentData) => {
    try {
      let apiPath = ''
      switch (boardType) {
        case 'free':
          apiPath = `${API_URL}/api/boards/articles/${postId}/comment_create/`
          break
        case 'info':
          apiPath = `${API_URL}/api/finance_infos/info/${postId}/comment_create/`
          break
        case 'news':
          throw new Error('뉴스는 댓글을 작성할 수 없습니다.')
        default:
          throw new Error('Invalid board type')
      }

      const response = await axios.post(
        apiPath,
        commentData,
        {
          headers: {
            Authorization: `Token ${authStore.token}`
          }
        }
      )

      if (!comments.value[postId]) {
        comments.value[postId] = []
      }
      const newComment = {
        id: response.data.id,
        content: response.data.content,
        author: response.data.username,
        created_at: response.data.created_at
      }
      comments.value[postId].push(newComment)

      const posts = getPosts(boardType)
      const postIndex = posts.findIndex(p => p.id === parseInt(postId))
      if (postIndex !== -1) {
        posts[postIndex].comment_count = (posts[postIndex].comment_count || 0) + 1
      }

      return newComment
    } catch (error) {
      console.error('댓글 작성 실패:', error)
      throw error
    }
  }

  // 8. 댓글 삭제
  const deleteComment = async (boardType, commentId) => {
    try {
      let apiPath = ''
      switch (boardType) {
        case 'free':
          apiPath = `${API_URL}/api/boards/comments/${commentId}/`
          break
        case 'info':
          apiPath = `${API_URL}/api/finance_infos/comments/${commentId}/`
          break
        case 'news':
          throw new Error('뉴스는 댓글을 삭제할 수 없습니다.')
        default:
          throw new Error('Invalid board type')
      }

      await axios.delete(apiPath, {
        headers: {
          Authorization: `Token ${authStore.token}`
        }
      })

      Object.keys(comments.value).forEach(postId => {
        const index = comments.value[postId].findIndex(c => c.id === commentId)
        if (index !== -1) {
          comments.value[postId].splice(index, 1)
        }
      })
    } catch (error) {
      console.error('댓글 삭제 실패:', error)
      throw error
    }
  }

  // 9. 좋아요 토글
  const toggleLike = async (boardType, postId) => {
    try {
      // 뉴스의 경우 로컬에서만 좋아요 상태 관리
      if (boardType === 'news') {
        const isCurrentlyLiked = likedPosts.value.includes(postId)
        if (isCurrentlyLiked) {
          likedPosts.value = likedPosts.value.filter(id => id !== postId)
        } else {
          if (!likedPosts.value.includes(postId)) {
            likedPosts.value.push(postId)
          }
        }
        localStorage.setItem('likedPosts', JSON.stringify(likedPosts.value))

        // 뉴스 목록에서 해당 게시글의 좋아요 개수 업데이트
        const posts = getPosts(boardType)
        const postIndex = posts.findIndex(p => p.id === parseInt(postId))
        if (postIndex !== -1) {
          posts[postIndex].like_count = isCurrentlyLiked ? 0 : 1
        }

        return !isCurrentlyLiked
      }

      let apiPath = ''
      switch (boardType) {
        case 'free':
          apiPath = `${API_URL}/api/boards/articles/${postId}/like/`
          break
        case 'info':
          apiPath = `${API_URL}/api/finance_infos/info/${postId}/like/`
          break
        default:
          throw new Error('Invalid board type')
      }

      const response = await axios.post(
        apiPath,
        {},
        { headers: { Authorization: `Token ${authStore.token}` } }
      )

      const isNowLiked = response.data.is_liked
      if (isNowLiked) {
        if (!likedPosts.value.includes(postId)) {
          likedPosts.value.push(postId)
        }
      } else {
        likedPosts.value = likedPosts.value.filter(id => id !== postId)
      }

      localStorage.setItem('likedPosts', JSON.stringify(likedPosts.value))

      const posts = getPosts(boardType)
      const postIndex = posts.findIndex(p => p.id === parseInt(postId))
      if (postIndex !== -1) {
        posts[postIndex].like_count = (posts[postIndex].like_count || 0) + (isNowLiked ? 1 : -1)
      }

      return isNowLiked
    } catch (error) {
      console.error('좋아요 처리 실패:', error)
      throw error
    }
  }

  // 임시 데이터 생성 함수 (Tags, Images 관련 필드 제거됨)
  const generateMockPosts = (boardType) => {
    const titles = {
      free: ['재테크 조언', '예금 금리 비교', '저축 목표', '주식 투자', '환율 전망'],
      news: ['금리 인상', '청년 금융', '디지털 뱅킹', '부동산', '가상화폐'],
      info: ['금리 비교 가이드', '재테크 시작', '은행 혜택', 'ISA 계좌', '연말정산']
    }
    const selectedTitles = titles[boardType] || titles.free
    return selectedTitles.map((title, index) => {
      const createdAt = new Date(Date.now() - index * 86400000).toISOString()
      return {
        id: Date.now() + index,
        title,
        content: `${title} 내용입니다.`,
        content_preview: `${title} 내용입니다...`,
        author: `사용자${index + 1}`,
        created_at: createdAt,
        updated_at: createdAt,
        comment_count: 0,
        is_notice: index === 0,
      }
    })
  }

  return {
    freePosts, newsPosts, infoPosts, comments, likedPosts,
    getPosts, getPost, getComments, isLiked, getLikedPosts,
    fetchPosts, fetchPostDetail, createPost, updatePost, deletePost,
    fetchComments, createComment, deleteComment, toggleLike
  }
})