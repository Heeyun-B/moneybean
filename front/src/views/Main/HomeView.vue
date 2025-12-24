<template>
  <div class="moneybean-container">
    <main class="content-wrapper">
      <div class="hero-section">
        
        <div class="banner-box" @mouseenter="stopSlide" @mouseleave="startSlide">
          <Transition name="fade">
            <div 
              :key="currentSlide" 
              class="banner-slide"
              @click="handleBannerClick"
            >
              <div class="banner-content">
                <span class="banner-tag">{{ banners[currentSlide].tag }}</span>
                <h2>{{ banners[currentSlide].title }}</h2>
                <p>{{ banners[currentSlide].desc }}</p>
              </div>
            </div>
          </Transition>
          
          <div class="banner-dots">
            <span 
              v-for="(banner, i) in banners" 
              :key="i" 
              :class="['dot', { active: currentSlide === i }]"
              @click.stop="goToSlide(i)" 
            ></span>
          </div>
        </div>

        <div class="login-box" v-if="!store.isAuthenticated">
          <div class="login-intro">
            <p class="intro-text">머니빈을 더 안전하고<br>편리하게 이용하세요.</p>
            <button class="login-move-btn" @click="router.push('/login')">
              <h3>머니빈 로그인</h3>
            </button>
          </div>
          <div class="login-footer">
            <div class="find-join">
              <span @click="router.push('/find-account')">아이디 찾기</span> |
              <span @click="router.push('/find-account')">비밀번호 찾기</span> |
              <span class="join-link" @click="router.push('/signup')">회원가입</span>
            </div>
          </div>
        </div>

        <div class="login-box profile-box" v-else>
          <div class="profile-content">
            <div class="profile-img-wrapper">
              <img src="@/assets/logo_bean.png" alt="프로필" class="profile-img">
            </div>
            <div class="welcome-text">
              <h3 class="user-name">{{ store.userNickname }}님</h3>
              <p class="greeting">오늘도 부자되세요! 🌱</p>
            </div>
            <div class="profile-actions">
              <button class="action-btn primary" @click="router.push({ name: 'assets' })">
                내 자산 보러가기
              </button>
              <button class="action-btn secondary" @click="handleLogout">
                로그아웃
              </button>
            </div>
          </div>
        </div>
      </div>

      <section class="pick-section">
        <div class="section-title-container">
          <img src="@/assets/logo_bean.png" alt="로고" class="section-logo">
          <h2 class="section-title">머니빈 Pick!</h2>
        </div>
        <div class="pick-grid">
          <div v-for="pick in picks" :key="pick.title" class="pick-card" @click="handlePickClick(pick.title)">
            <div class="pick-icon">{{ pick.icon }}</div>
            <div class="pick-name">{{ pick.title }}</div>
          </div>
        </div>
      </section>

      <section class="board-section">
        <div class="board-column">
          <div class="board-header">
            <h3>🗞️ 금융기사</h3>
            <span class="more-btn">더보기 ></span>
          </div>
          <ul class="board-list">
            <li v-for="n in 5" :key="n">머니빈 금융 뉴스 제목입니다 ({{n}})</li>
          </ul>
        </div>
        <div class="board-column">
          <div class="board-header">
            <h3>💡 금융정보</h3>
            <span class="more-btn">더보기 ></span>
          </div>
          <ul class="board-list">
            <li v-for="n in 5" :key="n">재테크 꿀팁: 이렇게 모아보세요 ({{n}})</li>
          </ul>
        </div>
      </section>
    </main>

    <footer class="main-footer">
      <div class="footer-content">
        <div class="footer-info">
          <p class="footer-copy-text">매일매일 쌓이는 금융 지식, 머니빈과 함께 똑똑한 자산 관리를 시작하세요.</p>
        </div>
        <div class="footer-copyright">
          &copy; 2025 — 머니빈 Team. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const store = useAuthStore()

const currentSlide = ref(0)
let slideInterval = null

// target 속성을 추가하여 클릭 시 이동할 페이지 지정
const banners = [
  { tag: 'QUIZ', title: '금융 퀴즈 챌린지!', desc: '매일 퀴즈 풀고 자산 나무에 물을 주세요.', target: 'quiz' },
  { tag: 'NEWS', title: '금리 인상 소식', desc: '나에게 유리한 예적금 상품을 찾아보세요.', target: 'deposit-list' },
  { tag: 'EVENT', title: '자산 관리 MBTI', desc: '당신의 투자 성향은 어떤 콩인가요?', target: 'assets' },
]

const picks = [
  { title: '자산관리', icon: '🏦' },
  { title: '카드', icon: '💳' },
  { title: '예적금', icon: '🐷' },
  { title: '투자', icon: '📈' },
]

// 배너 클릭 시 페이지 이동 함수
const handleBannerClick = () => {
  const target = banners[currentSlide.value].target
  if (target) {
    router.push({ name: target })
  }
}

const startSlide = () => {
  stopSlide()
  slideInterval = setInterval(() => {
    nextSlide()
  }, 3000)
}

const stopSlide = () => {
  if (slideInterval) clearInterval(slideInterval)
}

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % banners.length
}

const goToSlide = (index) => {
  currentSlide.value = index
  startSlide()
}

const handleLogout = () => {
  store.logOut()
  alert('로그아웃 되었습니다.')
}

const handlePickClick = (title) => {
  if (!store.isAuthenticated) {
    alert('로그인이 필요한 서비스입니다.')
    router.push('/login')
    return
  }
  switch (title) {
    case '예적금': router.push({ name: 'deposit-list' }); break
    case '자산관리':
    case '투자': router.push({ name: 'assets' }); break
    default: alert('준비 중인 서비스입니다.')
  }
}

onMounted(() => { startSlide() })
onUnmounted(() => { stopSlide() })
</script>

<style scoped>
* { font-family: 'GmarketSans'; }
.moneybean-container { background-color: #f8faf9; min-height: 100vh; color: #333; }
.content-wrapper { max-width: 1100px; margin: 0 auto; padding: 40px 20px; }
.hero-section { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-top: 20px; }
.banner-box { background: #00a651; border-radius: 20px; color: white; padding: 0; position: relative; min-height: 350px; display: flex; align-items: center; overflow: hidden; }
.banner-slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; padding: 40px 0 40px 40px; display: flex; flex-direction: column; justify-content: center; cursor: pointer; box-sizing: border-box; }
.banner-tag { background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; align-self: flex-start; }
.banner-content h2 { font-size: 32px; margin: 15px 0; font-weight: 700; }
.banner-content p { text-align: left; margin: 0; font-weight: 500; }
.banner-dots { position: absolute; bottom: 30px; left: 40px; display: flex; gap: 8px; z-index: 10; }
.dot { width: 8px; height: 8px; background: rgba(255,255,255,0.3); border-radius: 50%; cursor: pointer; transition: all 0.3s ease; }
.dot.active { background: white; width: 24px; border-radius: 10px; }
.login-box { background: white; border: 1px solid #eee; border-radius: 20px; padding: 30px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; min-height: 350px; }
.login-intro { width: 100%; margin-bottom: 25px; }
.intro-text { font-size: 15px; line-height: 1.5; color: #666; margin-bottom: 20px; font-weight: 500; }
.login-move-btn { width: 100%; max-width: 250px; background: #00a651; color: white; border: none; padding: 15px; border-radius: 8px; font-size: 16px; cursor: pointer; transition: all 0.2s; font-weight: 700; }
.login-move-btn:hover { background: #008e45; }
.find-join { font-size: 12px; color: #888; }
.find-join span { cursor: pointer; margin: 0 5px; }
.find-join span:hover { text-decoration: underline; color: #666; }
.profile-content { width: 100%; display: flex; flex-direction: column; align-items: center; }
.profile-img-wrapper { margin-bottom: 15px; }
.profile-img { width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 3px solid #f0f0f0; }
.welcome-text { margin-bottom: 30px; }
.user-name { font-size: 22px; color: #00a651; margin-bottom: 5px; font-weight: 700; }
.greeting { color: #666; font-size: 14px; margin: 0; font-weight: 500; }
.profile-actions { width: 100%; display: flex; flex-direction: column; gap: 10px; }
.action-btn { width: 100%; padding: 12px; border-radius: 8px; font-weight: 700; cursor: pointer; transition: 0.2s; border: none; font-size: 15px; }
.action-btn.primary { background-color: #00a651; color: white; }
.action-btn.secondary { background-color: #f5f5f5; color: #555; }
.pick-section { margin-top: 60px; }
.section-title-container { display: flex; align-items: center; margin-bottom: 20px; gap: 10px; }
.section-logo { width: 30px; height: 30px; border-radius: 50%; object-fit: cover;}
.section-title { font-size: 22px; margin: 0; font-weight: 700; }
.pick-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.pick-card { background: white; border: 1px solid #eee; border-radius: 20px; padding: 30px; text-align: center; cursor: pointer; transition: 0.3s; }
.pick-card:hover { transform: translateY(-5px); border-color: #00a651; }
.pick-icon { font-size: 30px; margin-bottom: 10px; }
.pick-name { font-weight: 500; }
.board-section { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 60px; }
.board-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 15px; }
.board-header h3 { font-weight: 700; }
.board-list { list-style: none; padding: 0; background: white; border-radius: 15px; border: 1px solid #eee; }
.board-list li { padding: 15px 20px; border-bottom: 1px solid #f5f5f5; font-size: 14px; cursor: pointer; font-weight: 500; }
.board-list li:hover { background: #fafafa; color: #00a651; }
.main-footer { background: #f8faf9; padding: 80px 20px; border-top: 1px solid #eee; margin-top: 100px; }
.footer-content { max-width: 1100px; margin: 0 auto; text-align: center; }
.footer-copy-text { font-size: 16px; color: #666; font-weight: 500; margin-bottom: 15px; letter-spacing: -0.5px; }
.footer-copyright { font-size: 13px; color: #aaa; font-weight: 300; }
.slide-fade-enter-active, .slide-fade-leave-active { transition: all 0.3s ease-in-out; }
.slide-fade-enter-from { opacity: 0; transform: translateX(30px); }
.slide-fade-leave-to { opacity: 0; transform: translateX(-30px); }
</style>