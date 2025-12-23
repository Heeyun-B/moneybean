<template>
  <YoutubeNavBar />
  
  <div class="detail-container">
    <button @click="goBack" class="btn-back">
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
      뒤로가기
    </button>
    
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      영상을 불러오는 중...
    </div>
    
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else class="detail-content">
      <div class="video-wrapper">
        <iframe
          :src="`https://www.youtube.com/embed/${videoId}`"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
          class="video-player"
        ></iframe>
      </div>
      
      <div class="video-info-section">
        <div class="info-header">
          <h1 class="video-title">{{ videoInfo.title }}</h1>
          <button @click="toggleSave" :class="['btn-save', { 'btn-cancel': isSaved }]">
            {{ isSaved ? '♥ 저장됨' : '♡ 나중에 보기' }}
          </button>
        </div>
        
        <div class="channel-info">
          <span class="channel-name">{{ videoInfo.channelTitle }}</span>
          <span class="upload-date">{{ formattedDate }}</span>
        </div>
        
        <div class="video-description">
          <div :class="['description-text', { 'expanded': isDescriptionExpanded }]">
            {{ videoInfo.description || '설명이 없습니다.' }}
          </div>
          <button 
            v-if="videoInfo.description && videoInfo.description.length > 100" 
            @click="isDescriptionExpanded = !isDescriptionExpanded" 
            class="btn-more"
          >
            {{ isDescriptionExpanded ? '접기' : '더보기' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import YoutubeNavBar from '@/components/youtube/YoutubeNavBar.vue'
import { getVideoDetails } from '@/api/youtube.js'

export default {
  name: 'VideoDetailView',
  components: {
    YoutubeNavBar
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const videoId = ref(route.params.id)
    const videoInfo = ref({
      title: '',
      channelTitle: '',
      description: '',
      thumbnail: '',
      publishedAt: ''
    })
    const loading = ref(true)
    const error = ref('')
    const savedVideos = ref([])
    const isDescriptionExpanded = ref(false)

    const loadSavedVideos = () => {
      const saved = localStorage.getItem('savedVideos')
      if (saved) {
        savedVideos.value = JSON.parse(saved)
      }
    }

    const isSaved = computed(() => {
      return savedVideos.value.some(v => v.id === videoId.value)
    })

    const formattedDate = computed(() => {
      if (!videoInfo.value.publishedAt) return ''
      const date = new Date(videoInfo.value.publishedAt)
      return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
    })

    const goBack = () => router.go(-1)

    const fetchVideoDetails = async () => {
      try {
        loading.value = true
        const video = await getVideoDetails(videoId.value)
        
        if (video && video.snippet) {
          videoInfo.value = {
            title: video.snippet.title,
            channelTitle: video.snippet.channelTitle,
            description: video.snippet.description,
            thumbnail: video.snippet.thumbnails.medium?.url || '',
            publishedAt: video.snippet.publishedAt
          }
        } else {
          error.value = '비디오 정보를 찾을 수 없습니다.'
        }
      } catch (err) {
        error.value = '영상을 불러오는데 실패했습니다.'
      } finally {
        loading.value = false
      }
    }

    const toggleSave = () => {
      if (isSaved.value) {
        savedVideos.value = savedVideos.value.filter(v => v.id !== videoId.value)
      } else {
        savedVideos.value.push({
          id: videoId.value,
          title: videoInfo.value.title,
          channelTitle: videoInfo.value.channelTitle,
          thumbnail: videoInfo.value.thumbnail
        })
      }
      localStorage.setItem('savedVideos', JSON.stringify(savedVideos.value))
    }

    onMounted(() => {
      loadSavedVideos()
      fetchVideoDetails()
    })

    return {
      videoId,
      videoInfo,
      loading,
      error,
      isSaved,
      toggleSave,
      goBack,
      formattedDate,
      isDescriptionExpanded
    }
  }
}
</script>

<style scoped>
.detail-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 30px 20px;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 5px;
  background: none;
  border: none;
  font-size: 16px;
  color: #666;
  cursor: pointer;
  margin-bottom: 15px;
  padding: 8px 15px;
  border-radius: 20px;
  transition: all 0.2s;
}

.btn-back:hover {
  background: #f1f1f1;
  color: #333;
}

.loading {
  text-align: center;
  padding: 100px 0;
  color: #888;
}

.video-wrapper {
  width: 100%;
  aspect-ratio: 16/9;
  background: #000;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
  margin-bottom: 24px;
}

.video-player {
  width: 100%;
  height: 100%;
}

.video-info-section {
  background: white;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 15px;
}

.video-title {
  font-size: 22px;
  font-weight: 700;
  color: #333;
  margin: 0;
  line-height: 1.4;
  flex: 1;
}

.btn-save {
  padding: 10px 20px;
  background: #e8f5e9;
  color: #2e7d32;
  border: 1px solid #a5d6a7;
  border-radius: 50px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  white-space: nowrap;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-save:hover {
  background: #c8e6c9;
  transform: scale(1.05);
}

.btn-cancel {
  background: #ffebee;
  color: #c62828;
  border-color: #ef9a9a;
}

.btn-cancel:hover {
  background: #ffcdd2;
}

.channel-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 20px;
}

.channel-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.upload-date {
  font-size: 14px;
  color: #888;
}

.video-description {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
}

.description-text {
  font-size: 15px;
  line-height: 1.7;
  color: #555;
  white-space: pre-wrap;
  word-break: break-word;
  
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.description-text.expanded {
  display: block;
}

.btn-more {
  background: none;
  border: none;
  color: #666;
  font-weight: 600;
  font-size: 14px;
  margin-top: 10px;
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
}

@media (max-width: 768px) {
  .info-header {
    flex-direction: column;
  }
  
  .btn-save {
    width: 100%;
    justify-content: center;
  }
}
</style>