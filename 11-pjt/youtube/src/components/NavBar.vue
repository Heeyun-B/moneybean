<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="logo">머니빈</router-link>
      
      <div class="nav-links">
        <router-link to="/" class="nav-link">홈</router-link>
        <router-link to="/search" class="nav-link">유튜브 검색</router-link>
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
  background-color: #9CCC65;
  padding: 0;
  box-shadow: 0 4px 10px rgba(139, 195, 74, 0.3);
  
  width: 100vw;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
}

.nav-container {
  max-width: 100%;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  height: 70px;
  box-sizing: border-box;
}

.logo {
  font-size: 28px;
  font-weight: bold;
  color: #33691E;
  text-decoration: none;
  transition: transform 0.3s;
}

.logo:hover {
  transform: scale(1.1);
}

.nav-links {
  display: flex;
  gap: 15px;
}

.nav-link {
  color: #33691E;
  text-decoration: none;
  font-size: 18px;
  font-weight: bold;
  
  padding: 10px 20px;
  border-radius: 30px;
  border-bottom: none;
  transition: all 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: #F1F8E9;
  color: #1B5E20;
  transform: translateY(-2px); /* 살짝 떠오르는 느낌 */
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
</style>