<template>
  <YoutubeNavBar />
  <div class="later-container">
    
    <div v-if="savedVideos.length === 0" class="no-videos">
      <img :src="emptyImage" alt="등록된 비디오가 없어요" class="empty-img" />
    </div>
    
    <div v-else class="video-grid">
      <div v-for="video in savedVideos" :key="video.id" class="video-item">
        <div class="video-card" @click="goToDetail(video.id)">
          <div class="thumbnail-wrapper">
            <img :src="video.thumbnail" :alt="video.title" class="thumbnail">
          </div>
          <div class="video-info">
            <h3 class="video-title">{{ video.title }}</h3>
            <p class="channel-name">{{ video.channelTitle }}</p>
          </div>
        </div>
        <button @click="removeVideo(video.id)" class="btn-delete">삭제</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import emptyImage from '@/assets/novideo.png'
import YoutubeNavBar from '@/components/youtube/YoutubeNavBar.vue'

export default {
  name: 'LaterView',
  components: {
    YoutubeNavBar
  },
  setup() {
    const router = useRouter()
    const savedVideos = ref([])

    const loadSavedVideos = () => {
      const saved = localStorage.getItem('savedVideos')
      if (saved) {
        savedVideos.value = JSON.parse(saved)
      }
    }

    const removeVideo = (videoId) => {
      if (confirm('이 영상을 삭제하시겠습니까?')) {
        savedVideos.value = savedVideos.value.filter(v => v.id !== videoId)
        localStorage.setItem('savedVideos', JSON.stringify(savedVideos.value))
      }
    }

    const goToDetail = (videoId) => {
      router.push(`/video/${videoId}`)
    }

    onMounted(() => {
      loadSavedVideos()
    })

    return {
      savedVideos,
      removeVideo,
      goToDetail,
      emptyImage
    }
  }
}
</script>

<style scoped>
.later-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 30px;
  color: #333;
}

.no-videos {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  min-height: 400px;
}

.empty-img {
  max-width: 300px;
  width: 100%;
  height: auto;
  object-fit: contain;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.video-item {
  position: relative;
}

.video-card {
  cursor: pointer;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  background: white;
  margin-bottom: 10px;
}

.video-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.thumbnail-wrapper {
  width: 100%;
  aspect-ratio: 16/9;
  overflow: hidden;
  background: #f1f1f1;
}

.thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-info {
  padding: 16px;
}

.video-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
  color: #333;
}

.channel-name {
  font-size: 13px;
  color: #777;
  margin: 0;
}

.btn-delete {
  width: 100%;
  padding: 12px;
  background: #ff6b6b;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: background 0.3s;
}

.btn-delete:hover {
  background: #fa5252;
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
  
  .page-title {
    font-size: 24px;
    text-align: center;
  }
}
</style>