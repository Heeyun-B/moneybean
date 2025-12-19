<template>
  <div class="youtube-layout">
    <YoutubeNavBar />

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

<script>
import YoutubeNavBar from '@/components/YoutubeNavBar.vue'
export default {
  name: 'YoutubeMainView',
  components: {
    YoutubeNavBar
  }
}
</script>

<style scoped>
.youtube-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.youtube-entry-container {
  flex: 1;
  max-width: 100%;
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
  justify-content: center;
  padding: 40px;
  width: 100%;
}

.bean-logo-bounce {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-bottom: 40px;
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
  animation: bounce 2s infinite;
  display: block;
}

.welcome-box h1 {
  font-size: 32px;
  margin-bottom: 15px;
  color: #00a651;
}

.welcome-box p {
  font-size: 18px;
  color: #666;
  margin-bottom: 40px;
}

.start-button {
  display: inline-block;
  padding: 15px 40px;
  background: #00a651; 
  color: white;
  text-decoration: none;
  border-radius: 50px; 
  font-size: 20px;
  font-weight: bold;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(0, 166, 81, 0.3);
}

.start-button:hover {
  background: #008e45;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 166, 81, 0.4);
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}
</style>