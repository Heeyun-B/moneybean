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

      </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const menus = ref([
  { title: '내 자산 보기', subs: ['내 자산 입력하기', '내 자산 한눈에 보기', 'AI 진단·추천받기'] },
  { title: '예·적금', subs: ['예적금 상품조회'] },
  { title: '금/은/달러', subs: ['국내 시세', '해외 시세'] },
  { title: '게시판', subs: ['자유게시판', '금융정보(꿀팁)', '금융기사'] },
  { title: '기타 편의', subs: ['주변은행찾기', '유튜브 찾기', '오늘의 금전운'] },
])

const goHome = () => {
  router.push({ name: 'home' })
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
    default:
      alert(`${sub} 메뉴는 준비 중입니다.`)
  }
}
</script>

<style scoped>
.navbar { background: white; border-bottom: 1px solid #eee; height: 80px; position: sticky; top: 0; z-index: 100; }
.nav-content { max-width: 1100px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; height: 100%; padding: 0 20px; }
.logo-area { display: flex; align-items: center; cursor: pointer; }
.bean-logo { width: 50px; height: 50px; border-radius: 50%; object-fit: cover; margin-right: 10px; }
.logo-text { font-size: 24px; font-weight: bold; color: #00a651; }

.menu-list { display: flex; gap: 20px; height: 100%; }
.menu-item { position: relative; height: 100%; display: flex; align-items: center; }
.menu-btn { background: none; border: none; font-size: 16px; font-weight: 600; cursor: pointer; padding: 10px; color: #333; }
.menu-btn:hover { color: #00a651; }

.submenu {
  display: none; position: absolute; top: 70px; left: 50%; transform: translateX(-50%);
  background: white; border: 1px solid #eee; list-style: none;
  padding: 10px 0; width: 160px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  border-radius: 8px; z-index: 101;
}
.menu-item:hover .submenu { display: block; }
.submenu li { padding: 10px 20px; font-size: 14px; cursor: pointer; color: #555; transition: 0.2s; }
.submenu li:hover { background: #f1fcf4; color: #00a651; font-weight: bold; }
</style>