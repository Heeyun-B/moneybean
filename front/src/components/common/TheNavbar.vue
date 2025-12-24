<template>
  <header class="navbar">
    <div class="nav-content">
      <div class="logo-area" @click="goHome">
        <img src="@/assets/logo_moneybean.png" alt="로고" class="bean-logo">
        <span class="logo-text">머니빈</span>
      </div>

      <nav class="menu-list">
        <div v-for="menu in menus" :key="menu.title" class="menu-item">
          <button class="menu-btn">{{ menu.title }}</button>
          <ul class="submenu">
            <li v-for="sub in menu.subs" :key="sub" @click="handleSubMenu(sub)">
              {{ sub }}
            </li>
          </ul>
        </div>
      </nav>

      <div class="profile-area">
        <div v-if="authStore.isAuthenticated" class="profile-menu">
          <div class="profile-trigger" @click="router.push({ name: 'profile' })">
            <img 
              :src="authStore.profileImage ? `${authStore.profileImage}?t=${new Date().getTime()}` : '/src/assets/logo_bean.png'" 
              alt="프로필" 
              class="profile-img"
            >
            <span class="profile-name">{{ authStore.userNickname }}님</span>
          </div>
          <ul class="profile-submenu">
            <li @click="router.push({ name: 'assets' })">내 자산 보기</li>
            <li @click="router.push({ name: 'profile' })">마이페이지</li>
            <li @click="router.push({ name: 'board-liked' })">좋아요한 글</li>
            <li @click="handleLogout" class="logout-item">로그아웃</li>
          </ul>
        </div>
        
        <div v-else class="auth-buttons">
          <button class="login-btn" @click="router.push({ name: 'login' })">로그인</button>
          <button class="signup-btn" @click="router.push({ name: 'signup' })">회원가입</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const menus = ref([
  { title: '내 자산 보기', subs: ['내 자산 입력하기', '내 자산 한눈에 보기', 'AI 진단·추천받기'] },
  { title: '예·적금', subs: ['예적금 상품조회'] },
  { title: '현물 자산', subs: ['금 시세 조회', '은 시세 조회'] },
  { title: '게시판', subs: ['자유게시판', '금융정보(꿀팁)', '금융기사', '좋아요한 글'] },
  { title: '기타 편의', subs: ['주변은행찾기', '유튜브 찾기', '오늘의 금전운'] },
])

const goHome = () => {
  router.push({ name: 'home' })
}

// 로그아웃 함수 하나로 통합
const handleLogout = () => {
  if (confirm('로그아웃 하시겠습니까?')) {
    authStore.logOut()
    router.push({ name: 'home' })
  }
}

const handleSubMenu = (sub) => {
  switch (sub) {
    case '유튜브 찾기':
      router.push({ name: 'youtube-home' })
      break
    case '내 자산 한눈에 보기':
      router.push({ name: 'assets' })
      break
    case '내 자산 입력하기':
      router.push({ name: 'asset-create' })
      break
    case '예적금 상품조회':
      router.push({ name: 'deposit-list' })
      break
    case '주변은행찾기':
      router.push({ name: 'map' })
      break
    case '금 시세 조회':
      router.push({ name: 'exchange', query: { asset: 'gold' } })
      break
    case '은 시세 조회':
      router.push({ name: 'exchange', query: { asset: 'silver' } })
      break
    case '자유게시판':
      router.push({ name: 'board-list', params: { type: 'free' } })
      break
    case '금융정보(꿀팁)':
      router.push({ name: 'board-list', params: { type: 'info' } })
      break
    case '금융기사':
      router.push({ name: 'board-list', params: { type: 'news' } })
      break
    case '좋아요한 글':
      router.push({ name: 'board-liked' })
      break
    case '오늘의 금전운':
      router.push({ name: 'luck' })
      break
    default:
      alert(`${sub} 메뉴는 준비 중입니다.`)
  }
}
</script>

<style scoped>
.navbar { background: white; border-bottom: 1px solid #eee; height: 80px; position: sticky; top: 0; z-index: 10000; }
.nav-content { max-width: 1100px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; height: 100%; padding: 0 20px; }
.logo-area { display: flex; align-items: center; cursor: pointer; }
.bean-logo { width: 50px; height: 50px; border-radius: 50%; object-fit: cover; margin-right: 10px; }
.logo-text { font-size: 24px; font-weight: bold; color: #00a651; }

.menu-list { display: flex; gap: 20px; height: 100%; }
.menu-item { position: relative; height: 100%; display: flex; align-items: center; }
.menu-btn { background: none; border: none; font-size: 16px; font-weight: 600; cursor: pointer; padding: 10px; color: #333; }
.menu-btn:hover { color: #00a651; }

.submenu {
  display: none; position: absolute; top: 60px; left: 50%; transform: translateX(-50%);
  background: white; border: 1px solid #eee; list-style: none;
  padding: 10px 0; width: 165px; box-shadow: 0 10px 25px rgba(0,0,0,0.15);
  border-radius: 8px; z-index: 10001;
}
.menu-item:hover .submenu { display: block; }
.submenu li { padding: 10px 20px; font-size: 14px; cursor: pointer; color: #555; transition: 0.2s; }
.submenu li:hover { background: #f1fcf4; color: #00a651; font-weight: bold; }

/* 프로필 영역 */
.profile-area { display: flex; align-items: center; height: 100%; }

.profile-menu { position: relative; height: 100%; display: flex; align-items: center; }
.profile-trigger {
  display: flex; align-items: center; gap: 8px; padding: 8px 12px;
  cursor: pointer; border-radius: 20px; transition: all 0.2s;
}
.profile-trigger:hover { background-color: #f8faf9; }
.profile-img { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; border: 2px solid #00a651; }
.profile-name { font-size: 15px; font-weight: 600; color: #333; }

.profile-submenu {
  display: none; position: absolute; top: 60px; right: 0;
  background: white; border: 1px solid #eee; list-style: none;
  padding: 10px 0; width: 150px; box-shadow: 0 10px 25px rgba(0,0,0,0.15);
  border-radius: 8px; z-index: 10001;
}
.profile-menu:hover .profile-submenu { display: block; }
.profile-submenu li {
  padding: 10px 20px; font-size: 14px; cursor: pointer;
  color: #555; transition: 0.2s;
}
.profile-submenu li:hover { background: #f1fcf4; color: #00a651; font-weight: bold; }
.profile-submenu li.logout-item { color: #ff6b6b; border-top: 1px solid #eee; }
.profile-submenu li.logout-item:hover { background: #fff5f5; color: #ff5252; }

/* 비로그인 상태 */
.auth-buttons { display: flex; gap: 10px; }
.login-btn, .signup-btn {
  padding: 8px 16px; border-radius: 8px; font-size: 14px;
  font-weight: 600; cursor: pointer; transition: all 0.2s; border: none;
}
.login-btn {
  background-color: white; color: #00a651;
  border: 1px solid #00a651;
}
.login-btn:hover { background-color: #f1fcf4; }
.signup-btn { background-color: #00a651; color: white; }
.signup-btn:hover { background-color: #008e45; }
</style>