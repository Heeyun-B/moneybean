<template>
  <div class="moneybean-container">
    <main class="content-wrapper">
      <div class="hero-section">
        
        <div class="banner-box">
          <div 
            v-for="(banner, i) in banners" 
            :key="i" 
            v-show="currentSlide === i" 
            class="banner-slide"
          >
            <div class="banner-content">
              <span class="banner-tag">{{ banner.tag }}</span>
              <h2>{{ banner.title }}</h2>
              <p>{{ banner.desc }}</p>
            </div>
          </div>
          
          <div class="banner-dots">
            <span 
              v-for="(banner, i) in banners" 
              :key="i" 
              :class="['dot', { active: currentSlide === i }]"
              @click="currentSlide = i"
            ></span>
          </div>
        </div>

        <div class="login-box" v-if="!store.isAuthenticated">
          <div class="login-intro">
            <p class="intro-text">머니빈을 더 안전하고<br>편리하게 이용하세요.</p>
            <button class="login-move-btn" @click="router.push('/login')">
              <strong>머니빈 로그인</strong>
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
              <p class="greeting">오늘도 부자 되세요! 🌱</p>
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
              <span class="badge new">NEW</span>
            </div>
            <h3 class="trending-title">{{ trendingPost.title }}</h3>
            <p class="trending-desc">{{ getPreviewText(trendingPost.content) }}</p>
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

    <footer class="main-footer">
      &copy; 2025 — MoneyBean Team. All rights reserved.
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useBoardStore } from '@/stores/board'

const router = useRouter()
const store = useAuthStore()
const boardStore = useBoardStore()

// --- 데이터 ---
const currentSlide = ref(0)
let slideInterval = null

const banners = [
  { tag: 'EVENT', title: '금융 퀴즈 챌린지!', desc: '매일 퀴즈 풀고 자산 나무에 물을 주세요.' },
  { tag: 'NEWS', title: '금리 인상 소식', desc: '나에게 유리한 예적금 상품을 찾아보세요.' },
  { tag: 'QUIZ', title: '자산 관리 MBTI', desc: '당신의 투자 성향은 어떤 콩인가요?' },
]

const picks = [
  { title: '자산관리', icon: '🏦' },
  { title: '카드', icon: '💳' },
  { title: '예적금', icon: '🐷' },
  { title: '투자', icon: '📈' },
]

// 게시판 데이터
const recentNews = computed(() => boardStore.getPosts('news').slice(0, 5))
const recentInfo = computed(() => boardStore.getPosts('info').slice(0, 5))

// [추가] 자유게시판 데이터 (최신 1개)
const trendingPost = computed(() => {
  const posts = boardStore.getPosts('free')
  return posts.length > 0 ? posts[0] : null
})

// [추가] 본문 미리보기 텍스트 처리
const getPreviewText = (content) => {
  if (!content) return ''
  const text = content.replace(/<[^>]*>?/gm, '') // HTML 태그 제거
  return text.length > 80 ? text.substring(0, 80) + '...' : text
}

// --- 메서드 ---
const startSlide = () => {
  slideInterval = setInterval(() => {
    currentSlide.value = (currentSlide.value + 1) % banners.length
  }, 4000)
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
    case '예적금':
      router.push({ name: 'deposit-list' })
      break
    case '자산관리':
    case '투자':
      router.push({ name: 'assets' })
      break
    default:
      alert('준비 중인 서비스입니다.')
  }
}

// --- 라이프사이클 훅 ---
onMounted(() => {
  startSlide()
  boardStore.fetchPosts('news')
  boardStore.fetchPosts('info')
  boardStore.fetchPosts('free') // [추가] 자유게시판 데이터 로드
})

onUnmounted(() => {
  if (slideInterval) clearInterval(slideInterval)
})
</script>

<style scoped>
.moneybean-container { background-color: #f8faf9; min-height: 100vh; color: #333; }
.content-wrapper { max-width: 1100px; margin: 0 auto; padding: 40px 20px; }

/* 배너 섹션 */
.hero-section { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-top: 20px; }
.banner-box { 
  background: #00a651; border-radius: 20px; color: white; padding: 40px;
  position: relative; min-height: 350px; display: flex; align-items: center;
}
.banner-slide { animation: fadeIn 0.8s; width: 100%; }
.banner-tag { background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
.banner-content h2 { font-size: 32px; margin: 15px 0; }
.banner-dots { position: absolute; bottom: 30px; left: 40px; display: flex; gap: 8px; }
.dot { width: 8px; height: 8px; background: rgba(255,255,255,0.3); border-radius: 50%; cursor: pointer; }
.dot.active { background: white; width: 24px; border-radius: 10px; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

/* 로그인/프로필 박스 */
.login-box { 
  background: white; border: 1px solid #eee; border-radius: 20px; padding: 30px;
  display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;
  min-height: 350px; 
}
.login-intro { width: 100%; margin-bottom: 25px; }
.intro-text { font-size: 15px; line-height: 1.5; color: #666; margin-bottom: 20px; }
.login-move-btn { width: 100%; max-width: 250px; background: #00a651; color: white; border: none; padding: 15px; border-radius: 8px; font-size: 16px; cursor: pointer; transition: all 0.2s; }
.login-move-btn:hover { background: #008e45; }
.find-join { font-size: 12px; color: #888; }
.find-join span { cursor: pointer; margin: 0 5px; }
.find-join span:hover { text-decoration: underline; color: #666; }

/* 프로필 박스 전용 스타일 */
.profile-content { width: 100%; display: flex; flex-direction: column; align-items: center; }
.profile-img-wrapper { margin-bottom: 15px; }
.profile-img { width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 3px solid #f0f0f0; }
.welcome-text { margin-bottom: 30px; }
.user-name { font-size: 22px; color: #00a651; margin-bottom: 5px; font-weight: bold; }
.greeting { color: #666; font-size: 14px; margin: 0; }
.profile-actions { width: 100%; display: flex; flex-direction: column; gap: 10px; }
.action-btn { width: 100%; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; border: none; font-size: 15px; }
.action-btn.primary { background-color: #00a651; color: white; }
.action-btn.primary:hover { background-color: #008e45; }
.action-btn.secondary { background-color: #f5f5f5; color: #555; }
.action-btn.secondary:hover { background-color: #e0e0e0; }

.pick-section { margin-top: 60px; }
.section-title-container { display: flex; align-items: center; margin-bottom: 20px; gap: 10px; position: relative; }
.section-logo { width: 30px; height: 30px; border-radius: 50%; object-fit: cover;}
.section-title { font-size: 22px; margin: 0; }
.pick-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.pick-card { background: white; border: 1px solid #eee; border-radius: 20px; padding: 30px; text-align: center; cursor: pointer; transition: 0.3s; }
.pick-card:hover { transform: translateY(-5px); border-color: #00a651; }
.pick-icon { font-size: 30px; margin-bottom: 10px; }

/* [추가] 트렌딩 섹션 스타일 */
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
.reaction-info { display: flex; gap: 12px; }
.trending-visual { font-size: 80px; opacity: 0.1; transform: rotate(-10deg); transition: 0.3s; }
.trending-card:hover .trending-visual { opacity: 0.2; transform: rotate(0deg) scale(1.1); }
@media (max-width: 768px) {
  .trending-card { flex-direction: column; text-align: left; }
  .trending-visual { display: none; }
  .trending-content { padding-right: 0; }
}

.board-section { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 60px; }
.board-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 15px; }
.board-list { list-style: none; padding: 0; background: white; border-radius: 15px; border: 1px solid #eee; }
.board-list li { padding: 15px 20px; border-bottom: 1px solid #f5f5f5; font-size: 14px; cursor: pointer; }
.board-list li:hover { background: #fafafa; color: #00a651; }
.more-btn { cursor: pointer; color: #00a651; font-size: 14px; }
.more-btn:hover { text-decoration: underline; }
.empty-board { color: #999; text-align: center; pointer-events: none; }
.main-footer { text-align: center; padding: 40px; color: #999; font-size: 12px; }
</style>