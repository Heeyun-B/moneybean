<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="logo">홈</router-link>
      
      
      <div class="nav-links">
        <router-link to="/youtube" class="nav-link">머니빈 TV</router-link>
        <router-link to="/youtube/search" class="nav-link">유튜브 검색</router-link>
        <router-link to="/later" class="nav-link">나중에 볼 영상</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>

<style scoped>
.navbar {
  background-color: white;
  width: 100%;
  height: 80px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  width: 100%;
  box-sizing: border-box;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #00a651;
  text-decoration: none;
  transition: transform 0.3s;
}

.logo:hover {
  transform: scale(1.05);
}

.nav-links {
  display: flex;
  gap: 10px;
}

.nav-link {
  color: #333;
  text-decoration: none;
  font-size: 16px;
  font-weight: bold;
  padding: 8px 16px;
  border-radius: 30px;
  border-bottom: none;
  transition: all 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: #f1fcf4;
  color: #00a651;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
</style>