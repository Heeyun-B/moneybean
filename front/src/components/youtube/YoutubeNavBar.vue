<template>
  <nav class="youtube-sub-nav">
    <div class="nav-content">
      <router-link to="/youtube" class="nav-item" exact-active-class="active">
        <span class="icon">🏠</span>
        <span class="text">홈</span>
      </router-link>
      
      <router-link to="/youtube/search" class="nav-item" active-class="active">
        <span class="icon">🔍</span>
        <span class="text">영상 검색</span>
      </router-link>
      
      <router-link to="/later" class="nav-item" active-class="active">
        <span class="icon">📂</span>
        <span class="text">나중에 볼 영상</span>
      </router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>

<style scoped>
.youtube-sub-nav {
  width: 100%;
  height: 60px;
  background-color: white;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 80px;
  z-index: 99;
  display: flex;
  align-items: center;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 10px;
  padding: 0 20px;
  width: 100%;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  text-decoration: none;
  color: #555;
  border-radius: 20px;
  transition: all 0.2s ease;
  gap: 8px;
}

.nav-item:hover {
  background-color: #f5f5f5;
}

.nav-item.active {
  background-color: #f1fcf4;
  color: #00a651;
  font-weight: bold;
}

.icon {
  font-size: 18px;
}

.text {
  font-size: 14px;
}
</style>