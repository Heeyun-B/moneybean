<template>
  <YoutubeNavBar />
  
  <div class="search-container">
    <div class="search-header" @click="$router.push({ name: 'youtube-home' })" title="뒤로가기">
      <button class="back-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M15 18l-6-6 6-6"/>
        </svg>
      </button>
      <h2 class="page-title">유튜브 검색</h2>
    </div>

    
    <div class="search-wrapper">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          @keyup.enter="handleSearch"
          type="text" 
          placeholder="유튜브에서 영상 찾기"
          class="search-input"
        >
        <button @click="handleSearch" class="search-button">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">🫛 열심히 찾는 중...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="videos.length > 0" class="video-grid">
      <VideoCard 
        v-for="video in videos" 
        :key="video.id.videoId"
        :video="video"
        @click="goToDetail(video)"
      />
    </div>

    <div v-if="!loading && videos.length === 0 && searchQuery" class="no-results">
      검색 결과가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import YoutubeNavBar from '@/components/youtube/YoutubeNavBar.vue'
import VideoCard from '@/components/youtube/VideoCard.vue'
import { searchVideos } from '@/api/youtube.js'

const router = useRouter()
const searchQuery = ref('')
const videos = ref([])
const loading = ref(false)
const error = ref('')

// 세션스토리지에서 검색 상태 복원
const restoreSearchState = () => {
  const token = localStorage.getItem('token')
  if (!token) {
    searchQuery.value = ''
    videos.value = []
    return
  }

  const savedQuery = sessionStorage.getItem('youtube_search_query')
  const savedVideos = sessionStorage.getItem('youtube_search_videos')

  if (savedQuery) {
    searchQuery.value = savedQuery
  }
  if (savedVideos) {
    try {
      videos.value = JSON.parse(savedVideos)
    } catch (e) {
      console.error('검색 결과 복원 실패:', e)
    }
  }
}

// 검색 상태 저장
const saveSearchState = () => {
  sessionStorage.setItem('youtube_search_query', searchQuery.value)
  sessionStorage.setItem('youtube_search_videos', JSON.stringify(videos.value))
}

const handleSearch = async () => {
  if (!searchQuery.value.trim()) return
  loading.value = true
  try {
    videos.value = await searchVideos(searchQuery.value)
    saveSearchState()
  } catch (err) {
    error.value = '데이터를 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

const goToDetail = (video) => {
  saveSearchState() // 상세 페이지로 이동하기 전에 상태 저장
  router.push(`/video/${video.id.videoId}`)
}

onMounted(() => {
  restoreSearchState()
})

onBeforeUnmount(() => {
  saveSearchState()
})
</script>

<style scoped>
.search-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.search-header {
  display: inline-flex;;
  align-items: center;
  margin-bottom: 40px;
  gap: 1px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.search-header:hover {
  opacity: 0.7;
}

.back-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: transparent;
  border: none;
  border-radius: 50%;
  color: #00a651;
  pointer-events: none;
}

.search-header:hover .back-button {
  background-color: rgba(139, 195, 74, 0.2);
  transform: translateX(-3px);
}

.page-title {
  font-size: 28px;
  margin: 0;
  color: #00a651;
  font-weight: bold;
  user-select: none;
}

.search-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 50px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  max-width: 700px;
  position: relative;
}

.search-input {
  flex: 1;
  padding: 15px 25px;
  font-size: 18px;
  border: 2px solid #DCEDC8;
  border-radius: 50px;
  background-color: white;
  transition: all 0.3s;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.search-input:focus {
  outline: none;
  border-color: #8BC34A;
  box-shadow: 0 4px 12px rgba(139, 195, 74, 0.3);
}

.search-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 54px;
  height: 54px;
  background: #00a651;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 6px rgba(139, 195, 74, 0.4);
  flex-shrink: 0;
}

.search-button:hover {
  background: #7CB342;
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(139, 195, 74, 0.6);
}

.loading {
  text-align: center;
  padding: 60px;
  font-size: 20px;
  color: #558B2F;
}

.bean-spinner {
  display: inline-block;
  animation: spin 1s infinite linear;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: 20px;
  background: #FFEBEE;
  color: #D32F2F;
  border-radius: 12px;
  margin-bottom: 20px;
  font-weight: bold;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 25px;
  margin-bottom: 40px;
}

.no-results {
  text-align: center;
  padding: 60px;
  font-size: 18px;
  color: #888;
}

@media (max-width: 1200px) {
  .video-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .video-grid {
    grid-template-columns: 1fr;
  }
  
  .search-input {
    font-size: 16px;
    padding: 12px 20px;
  }
  
  .search-button {
    width: 46px;
    height: 46px;
  }
}
</style>