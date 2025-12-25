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
              <img
                :src="banners[currentSlide].img"
                alt="배너 이미지"
                class="banner-full-image"
              >
            </div>
          </Transition>

          <div class="banner-dots">
            <span
              v-for="(_, i) in banners"
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
            <div class="profile-header">
              <div class="profile-img-wrapper" @click="router.push({ name: 'profile' })">
                <img
                  :src="store.profileImage || '/src/assets/logo_bean.png'"
                  alt="프로필"
                  class="profile-img"
                >
              </div>
              <div class="welcome-text">
                <h3 class="user-name">{{ store.userNickname }}님</h3>
                <p class="greeting">오늘도 부자되세요! 🌱</p>
              </div>
            </div>
            <div class="profile-actions">
              <button class="action-btn primary" @click="router.push({ name: 'assets' })">
                <span class="btn-icon">💰</span>
                <span class="btn-text">내 자산 관리</span>
              </button>
              <button class="action-btn secondary" @click="router.push({ name: 'profile' })">
                <span class="btn-icon">👤</span>
                <span class="btn-text">마이페이지</span>
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

      <section class="trending-section" v-if="trendingPost">
        <div class="section-title-container">
          <span class="section-icon">🔥</span>
          <h2 class="section-title">지금 뜨는 이야기</h2>
          <span class="more-link" @click="router.push({ name: 'board-list', params: { type: 'free' } })">자유게시판 전체보기 ></span>
        </div>
        
        <div class="trending-card" @click="router.push({ name: 'board-detail', params: { type: 'free', id: trendingPost.id } })">
          <div class="trending-content">
            <div class="trending-badges">
              <span class="badge free">자유게시판</span>
              <span class="badge hot">🔥 HOT</span>
            </div>
            <h3 class="trending-title">{{ trendingPost.title }}</h3>
            <div class="trending-meta">
              <span class="author-info">🖊️ {{ trendingPost.author }}</span>
              <div class="reaction-info">
                <span>❤️ {{ trendingPost.like_count || 0 }}</span>
                <span>💬 {{ trendingPost.comment_count || 0 }}</span>
              </div>
            </div>
          </div>
          <div class="trending-visual">
            <span class="visual-icon">💬</span>
          </div>
        </div>
      </section>

      <section class="board-section">
        <div class="board-column">
          <div class="board-header">
            <h3>🗞️ 금융기사</h3>
            <span class="more-btn" @click="router.push({ name: 'board-list', params: { type: 'news' } })">더보기 ></span>
          </div>
          <ul class="board-list">
            <li
              v-for="post in recentNews"
              :key="post.id"
              @click="router.push({ name: 'board-detail', params: { type: 'news', id: post.id } })"
            >
              {{ post.title }}
            </li>
            <li v-if="recentNews.length === 0" class="empty-board">등록된 기사가 없습니다</li>
          </ul>
        </div>
        <div class="board-column">
          <div class="board-header">
            <h3>💡 금융정보</h3>
            <span class="more-btn" @click="router.push({ name: 'board-list', params: { type: 'info' } })">더보기 ></span>
          </div>
          <ul class="board-list">
            <li
              v-for="post in recentInfo"
              :key="post.id"
              @click="router.push({ name: 'board-detail', params: { type: 'info', id: post.id } })"
            >
              {{ post.title }}
            </li>
            <li v-if="recentInfo.length === 0" class="empty-board">등록된 정보가 없습니다</li>
          </ul>
        </div>
      </section>
    </main>

    <!-- 외부 리다이렉트 로딩 오버레이 -->
    <Transition name="fade">
      <div v-if="isRedirecting" class="redirect-overlay">
        <div class="redirect-modal">
          <div class="spinner"></div>
          <p class="redirect-message">{{ loadingMessage }}</p>
        </div>
      </div>
    </Transition>

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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useBoardStore } from '@/stores/board'
import quizImg from '@/assets/banner_imgs/quiz_img.png'
import fortuneImg from '@/assets/banner_imgs/fortune_img.png'
import balanceImg from '@/assets/banner_imgs/balance_img.png'

const router = useRouter()
const store = useAuthStore()
const boardStore = useBoardStore()

const currentSlide = ref(0)
let slideInterval = null

// 외부 리다이렉트 상태
const isRedirecting = ref(false)
const loadingMessage = ref('')
let redirectTimer = null

// 배너 이미지와 이동 페이지 지정
const banners = [
  { img: quizImg, target: 'quiz' },
  { img: balanceImg, target: 'assets' },
  { img: fortuneImg, target: 'luck' },
]

const picks = [
  { title: '자산관리', icon: '🏦' },
  { title: '예적금', icon: '🐷' },
  { title: '카드', icon: '💳' },
  { title: '투자', icon: '📈' },
]

// 배너 클릭 시 페이지 이동 함수
const handleBannerClick = () => {
  const target = banners[currentSlide.value].target
  if (target) {
    router.push({ name: target })
  }
}

// 게시판 데이터
const recentNews = computed(() => boardStore.getPosts('news').slice(0, 5))
const recentInfo = computed(() => boardStore.getPosts('info').slice(0, 5))

// 자유게시판 데이터 - 가장 많은 좋아요를 받은 글
const trendingPost = computed(() => {
  const posts = boardStore.getPosts('free')
  if (posts.length === 0) return null

  // 좋아요 수로 내림차순 정렬, 동일하면 최신순
  const sortedPosts = [...posts].sort((a, b) => {
    if (b.like_count !== a.like_count) {
      return b.like_count - a.like_count
    }
    return new Date(b.created_at) - new Date(a.created_at)
  })

  return sortedPosts[0]
})

// 메서드
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

const handlePickClick = (title) => {
  if (!store.isAuthenticated) {
    alert('로그인이 필요한 서비스입니다.')
    router.push('/login')
    return
  }
  switch (title) {
    case '예적금':
      router.push({ name: 'deposit-list' })
      break
    case '자산관리':
      router.push({ name: 'assets' })
      break
    case '카드':
      startExternalRedirect('https://card-lounge.toss.im/', '토스 카드 추천 서비스로 이동 중입니다...')
      break
    case '투자':
      startExternalRedirect('https://www.tossinvest.com/', '토스 증권으로 이동 중입니다...')
      break
    default:
      alert('준비 중인 서비스입니다.')
  }
}

// 외부 리다이렉트 시작
const startExternalRedirect = (url, message) => {
  isRedirecting.value = true
  loadingMessage.value = message

  redirectTimer = setTimeout(() => {
    window.location.href = url
  }, 1500)
}

// 라이프사이클 훅
onMounted(() => {
  startSlide()
  boardStore.fetchPosts('news')
  boardStore.fetchPosts('info')
  boardStore.fetchPosts('free')
})

onUnmounted(() => {
  stopSlide()
  if (redirectTimer) clearTimeout(redirectTimer)
})
</script>

<style scoped>
* { font-family: 'GmarketSans'; }
.moneybean-container { background-color: #f8faf9; min-height: 100vh; color: #333; }
.content-wrapper { max-width: 1100px; margin: 0 auto; padding: 40px 20px; }
.hero-section { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-top: 20px; }

/* 배너 박스 - 확실히 둥글게 */
.banner-box { 
  background: white; 
  border-radius: 20px; 
  color: white; 
  padding: 0; 
  position: relative; 
  height: 330px;
  display: flex; 
  align-items: center; 
  justify-content: center;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  border: 1px solid #f0f0f0;
}

.banner-slide { 
  position: absolute; 
  top: 0; 
  left: 0; 
  right: 0;
  bottom: 0;
  width: 100%; 
  height: 100%; 
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* 배너 이미지 - 확실히 둥글게 */
.banner-full-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center center;
}

.banner-dots { 
  position: absolute; 
  bottom: 30px; 
  left: 40px; 
  display: flex; 
  gap: 8px; 
  z-index: 10; 
}

.dot { 
  width: 8px; 
  height: 8px; 
  background: rgba(255,255,255,0.3); 
  border-radius: 50%; 
  cursor: pointer; 
  transition: all 0.3s ease; 
}

.dot.active { 
  background: white; 
  width: 24px; 
  border-radius: 10px; 
}

.login-box {
  background: white;
  border: 1px solid #eee;
  border-radius: 20px;
  padding: 25px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  height: 330px;
}

.login-intro { width: 100%; margin-bottom: 25px; }
.intro-text { font-size: 15px; line-height: 1.5; color: #666; margin-bottom: 20px; font-weight: 500; }
.login-move-btn { width: 100%; max-width: 250px; background: #00a651; color: white; border: none; padding: 15px; border-radius: 8px; font-size: 16px; cursor: pointer; transition: all 0.2s; font-weight: 700; }
.login-move-btn:hover { background: #008e45; }
.login-move-btn h3 { margin: 0; font-size: 16px; }
.logout-text-btn { background: none; border: none; color: #999; font-size: 13px; text-decoration: underline; cursor: pointer; margin-top: 5px; }
.find-join { font-size: 12px; color: #888; }
.find-join span { cursor: pointer; margin: 0 5px; }
.find-join span:hover { text-decoration: underline; color: #666; }
.join-link { font-weight: 600; color: #00a651; }

.profile-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 0;
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding-top: 20px;
}

.profile-img-wrapper {
  cursor: pointer;
  transition: all 0.3s ease;
}

.profile-img-wrapper:hover {
  transform: translateY(-2px);
}

.profile-img {
  width: 75px;
  height: 75px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #e8f5e9;
  box-shadow: 0 2px 12px rgba(0, 166, 81, 0.15);
}

.welcome-text {
  text-align: center;
  line-height: 1.4;
}

.user-name {
  font-size: 19px;
  color: #00a651;
  margin: 0 0 4px 0;
  font-weight: 800;
  letter-spacing: -0.3px;
}

.greeting {
  color: #666;
  font-size: 13px;
  margin: 0;
  font-weight: 400;
}

.profile-actions {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-bottom: 5px;
}

.action-btn {
  width: 100%;
  padding: 12px 16px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
}

.btn-icon {
  font-size: 16px;
  line-height: 1;
}

.btn-text {
  font-weight: 700;
  letter-spacing: -0.2px;
  font-size: 14px;
}

.action-btn.primary {
  background: linear-gradient(135deg, #00a651 0%, #008e45 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 166, 81, 0.2);
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3);
}

.action-btn.secondary {
  background-color: #fff;
  color: #555;
  border: 2px solid #e8e8e8;
}

.action-btn.secondary:hover {
  background-color: #f8f9fa;
  border-color: #00a651;
  color: #00a651;
  transform: translateY(-2px);
}

.pick-section { margin-top: 60px; }
.section-title-container { display: flex; align-items: center; margin-bottom: 20px; gap: 10px; position: relative; }
.section-logo { width: 30px; height: 30px; border-radius: 50%; object-fit: cover;}
.section-title { font-size: 22px; margin: 0; font-weight: 700; }
.pick-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.pick-card { background: white; border: 1px solid #eee; border-radius: 20px; padding: 30px; text-align: center; cursor: pointer; transition: 0.3s; }
.pick-card:hover { transform: translateY(-5px); border-color: #00a651; box-shadow: 0 8px 20px rgba(0, 166, 81, 0.1); }
.pick-icon { font-size: 30px; margin-bottom: 10px; }
.pick-name { font-weight: 500; }

/* 트렌딩 섹션 */
.trending-section { margin-top: 60px; }
.section-icon { font-size: 24px; }
.more-link { margin-left: auto; font-size: 14px; color: #999; cursor: pointer; transition: 0.2s; }
.more-link:hover { color: #00a651; }

.trending-card {
  background: white; border-radius: 20px; padding: 35px; border: 1px solid #eee;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03); cursor: pointer;
  display: flex; justify-content: space-between; align-items: center;
  transition: all 0.3s ease; position: relative; overflow: hidden;
}
.trending-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0, 166, 81, 0.15); border-color: #00a651; }
.trending-content { flex: 1; padding-right: 20px; z-index: 1; }
.trending-badges { display: flex; gap: 8px; margin-bottom: 15px; }
.badge { font-size: 12px; font-weight: bold; padding: 4px 10px; border-radius: 12px; }
.badge.free { background-color: #e8f5e9; color: #00a651; }
.badge.new { background-color: #ff6b6b; color: white; }
.trending-title { font-size: 24px; font-weight: bold; margin: 0 0 10px 0; color: #333; }
.trending-desc { font-size: 15px; color: #666; line-height: 1.6; margin-bottom: 20px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.trending-meta { display: flex; align-items: center; gap: 20px; font-size: 14px; color: #888; }
.author-info { display: flex; align-items: center; gap: 5px; }
.reaction-info { display: flex; gap: 12px; }
.trending-visual { font-size: 80px; opacity: 0.1; transform: rotate(-10deg); transition: 0.3s; }
.trending-card:hover .trending-visual { opacity: 0.2; transform: rotate(0deg) scale(1.1); }

.board-section { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 60px; }
.board-column { }
.board-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 15px; }
.board-header h3 { font-weight: 700; margin: 0; }
.board-list { list-style: none; padding: 0; margin: 0; background: white; border-radius: 15px; border: 1px solid #eee; }
.board-list li { padding: 15px 20px; border-bottom: 1px solid #f5f5f5; font-size: 14px; cursor: pointer; font-weight: 500; transition: 0.2s; }
.board-list li:hover { background: #fafafa; color: #00a651; }
.board-list li:last-child { border-bottom: none; }

.main-footer { background: #f8faf9; padding: 80px 20px; border-top: 1px solid #eee; margin-top: 100px; }
.footer-content { max-width: 1100px; margin: 0 auto; text-align: center; }
.footer-info { margin-bottom: 20px; }
.footer-copy-text { font-size: 16px; color: #666; font-weight: 500; margin: 0 0 15px 0; letter-spacing: -0.5px; }
.footer-copyright { font-size: 13px; color: #aaa; font-weight: 300; margin: 0; }
.more-btn { cursor: pointer; color: #00a651; font-size: 14px; font-weight: 600; }
.more-btn:hover { text-decoration: underline; }
.empty-board { color: #999; text-align: center; pointer-events: none; }

/* 페이드 애니메이션 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 외부 리다이렉트 오버레이 */
.redirect-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.redirect-modal {
  background: white;
  padding: 50px 60px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #00a651;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.redirect-message {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

/* 반응형 */
@media (max-width: 1024px) {
  .hero-section { grid-template-columns: 1fr; }
  .banner-box, .login-box { height: 350px; }
  .pick-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .banner-box, .login-box { height: 300px; }
  .pick-grid { grid-template-columns: 1fr 1fr; }
  .board-section { grid-template-columns: 1fr; }
  .trending-card { flex-direction: column; text-align: left; }
  .trending-visual { display: none; }
  .trending-content { padding-right: 0; }
}
</style>