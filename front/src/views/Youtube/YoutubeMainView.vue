<template>
  <YoutubeNavBar />

  <div class="youtube-layout">
    <div class="youtube-entry-container">
      <div class="welcome-box">
        <img src="@/assets/logo_moneybean.png" alt="머니빈 로고" class="bean-logo-bounce">
        <router-link to="/youtube/search" class="start-button">
          유튜브 검색하러 가기
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import YoutubeNavBar from '@/components/youtube/YoutubeNavBar.vue'
const router = useRouter()
</script>

<style scoped>
.youtube-layout {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 140px);
  background-color: #fcfcfc;
}

.youtube-entry-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.welcome-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  animation: fadeIn 1.2s ease-out;
}

.logo-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  margin-bottom: 80px;
  align-items: center;
}

.bean-logo-bounce {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  position: relative;
  z-index: 2;
  animation: bounce 3.5s infinite ease-in-out;
}

.logo-shadow {
  width: 100px;
  height: 15px;
  background: rgba(0,0,0,0.1);
  border-radius: 50%;
  margin: 10px auto 0;
  animation: shadowSize 3.5s infinite ease-in-out;
}

.entry-title {
  font-size: 28px;
  font-weight: 800;
  color: #333;
  margin-bottom: 15px;
}

.entry-sub {
  font-size: 16px;
  color: #888;
  margin-bottom: 60px;
}

.start-button {
  display: inline-block;
  padding: 16px 50px;
  background: #00a651; 
  color: white;
  text-decoration: none;
  border-radius: 50px; 
  font-size: 18px;
  font-weight: bold;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 8px 20px rgba(0, 166, 81, 0.2);
}

.start-button:hover {
  background: #008e45;
  transform: translateY(-5px);
  box-shadow: 0 12px 25px rgba(0, 166, 81, 0.3);
}

@keyframes bounce {
  0%, 100% { transform: translateY(-20px); }
  50% { transform: translateY(-40px); }
}

@keyframes shadowSize {
  0%, 100% { transform: scale(0.85); opacity: 0.25; }
  50% { transform: scale(0.7); opacity: 0.15; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>