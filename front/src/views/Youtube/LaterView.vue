<template>
  <YoutubeNavBar />
  <div class="later-container">
    <!-- 비로그인 사용자 안내 -->
    <div v-if="!authStore.isAuthenticated" class="login-required">
      <div class="login-box">
        <h2>로그인이 필요한 서비스입니다</h2>
        <p>나중에 볼 영상을 저장하려면 로그인해주세요.</p>
        <button @click="goToLogin" class="btn-login">로그인하기</button>
      </div>
    </div>

    <!-- 로그인 사용자 -->
    <template v-else>
      <div v-if="savedVideos.length === 0" class="no-videos">
        <img :src="emptyImage" alt="비디오 없음" class="empty-img" />
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
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import YoutubeNavBar from '@/components/youtube/YoutubeNavBar.vue'
import emptyImage from '@/assets/novideo.png'

const router = useRouter()
const authStore = useAuthStore()
const savedVideos = ref([])

// 사용자별 localStorage 키 생성
const getStorageKey = () => {
  if (!authStore.isAuthenticated || !authStore.userNickname) {
    return null
  }
  return `savedVideos_${authStore.userNickname}`
}

const loadSavedVideos = () => {
  // 로그인하지 않은 경우 데이터를 로드하지 않음
  if (!authStore.isAuthenticated) {
    savedVideos.value = []
    return
  }

  const storageKey = getStorageKey()
  if (!storageKey) {
    savedVideos.value = []
    return
  }

  const saved = localStorage.getItem(storageKey)
  if (saved) {
    try {
      savedVideos.value = JSON.parse(saved)
    } catch (e) {
      console.error('저장된 영상 데이터 파싱 실패:', e)
      savedVideos.value = []
    }
  } else {
    savedVideos.value = []
  }
}

const removeVideo = (videoId) => {
  if (!authStore.isAuthenticated) return

  if (confirm('삭제하시겠습니까?')) {
    savedVideos.value = savedVideos.value.filter(v => v.id !== videoId)
    const storageKey = getStorageKey()
    if (storageKey) {
      localStorage.setItem(storageKey, JSON.stringify(savedVideos.value))
    }
  }
}

const goToDetail = (videoId) => {
  router.push(`/video/${videoId}`)
}

const goToLogin = () => {
  router.push({ name: 'login', query: { redirect: '/later' } })
}

onMounted(loadSavedVideos)
</script>

<style scoped>
.later-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
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

/* 로그인 필요 화면 */
.login-required {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 500px;
  padding: 40px 20px;
}

.login-box {
  text-align: center;
  background: white;
  padding: 60px 40px;
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}

.login-box h2 {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 16px;
}

.login-box p {
  font-size: 16px;
  color: #666;
  margin-bottom: 30px;
  line-height: 1.6;
}

.btn-login {
  padding: 14px 40px;
  background: #00a651;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(0, 166, 81, 0.3);
}

.btn-login:hover {
  background: #008e45;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 166, 81, 0.4);
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