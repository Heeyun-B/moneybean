<template>
  <YoutubeNavBar />
  <div class="search-container">
    <div class="search-header">
      <button class="back-button" @click="$router.push('/')" title="뒤로가기">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M15 18l-6-6 6-6"/>
        </svg>
      </button>
      
      <h1 class="page-title">유튜브 검색</h1>
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
        <button @click="handleSearch" class="search-button" title="검색">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">
       <span class="bean-spinner">🫛</span> 열심히 찾는 중...
    </div>
    
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

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import VideoCard from '@/components/youtube/VideoCard.vue'
import YoutubeNavBar from '@/components/youtube/YoutubeNavBar.vue'
import { searchVideos } from '@/api/youtube.js'

export default {
  name: 'SearchView',
  components: {
    VideoCard,
    YoutubeNavBar
  },
  setup() {
    const router = useRouter()
    const searchQuery = ref('')
    const videos = ref([])
    const loading = ref(false)
    const error = ref('')

    const handleSearch = async () => {
      if (!searchQuery.value.trim()) {
        alert('검색어를 입력해주세요')
        return
      }

      loading.value = true
      error.value = ''
      
      try {
        const results = await searchVideos(searchQuery.value)
        videos.value = results
      } catch (err) {
        error.value = 'API 호출에 실패했습니다. API Key를 확인해주세요.'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const goToDetail = (video) => {
      router.push(`/video/${video.id.videoId}`)
    }

    return {
      searchQuery,
      videos,
      loading,
      error,
      handleSearch,
      goToDetail
    }
  }
}
</script>

<style scoped>
.search-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.search-header {
  display: flex;
  align-items: center;
  margin-bottom: 40px;
  gap: 15px;
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
  cursor: pointer;
  color: #00a651;
  transition: all 0.2s;
}

.back-button:hover {
  background-color: rgba(139, 195, 74, 0.2);
  transform: translateX(-3px);
}

.page-title {
  font-size: 28px;
  margin: 0;
  color: #00a651;
  font-weight: bold;
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