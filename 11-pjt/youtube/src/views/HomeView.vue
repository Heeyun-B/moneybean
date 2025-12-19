<template>
  <div class="home">
    <div class="welcome-container">
      <div class="bean-icon">🫛</div>
      
      <h1>머니빈 홈은 지금 자라나는 중이에요!</h1>
      <p>홈 화면은 준비 중이니, 검색 기능을 먼저 이용해 보세요.</p>
      
      <router-link to="/search" class="start-button">
        유튜브 검색하러 가기
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.welcome-container {
  text-align: center;
  padding: 40px;
}

.bean-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: bounce 2s infinite;
}

.welcome-container h1 {
  font-size: 32px;
  margin-bottom: 15px;
  color: #33691E; 
}

.welcome-container p {
  font-size: 18px;
  color: #558B2F;
  margin-bottom: 40px;
}

.start-button {
  display: inline-block;
  padding: 15px 40px;
  background: #8BC34A; 
  color: white;
  text-decoration: none;
  border-radius: 50px; 
  font-size: 20px;
  font-weight: bold;
  transition: all 0.3s;
  box-shadow: 0 4px 6px rgba(139, 195, 74, 0.4);
}

.start-button:hover {
  background: #7CB342;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(139, 195, 74, 0.6);
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>