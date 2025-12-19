<template>
  <div class="moneybean-container">
    <header class="navbar">
      <div class="nav-content">
        <div class="logo-area" @click="$router.push('/')">
          <img src="@/assets/logo_moneybean.png" alt="로고" class="bean-logo">
          <span class="logo-text">머니빈</span>
        </div>
        
        <nav class="menu-list">
          <div v-for="menu in menus" :key="menu.title" class="menu-item">
            <button class="menu-btn">{{ menu.title }}</button>
            <ul class="submenu">
              <li v-for="sub in menu.subs" :key="sub">{{ sub }}</li>
            </ul>
          </div>
        </nav>
      </div>
    </header>

    <main class="content-wrapper">
      <div class="hero-section">
        <div class="banner-box">
          <div v-for="(banner, i) in banners" :key="i" v-show="currentSlide === i" class="banner-slide">
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

        <div class="login-box">
          <h3>로그인</h3>
          <input type="text" placeholder="ID" class="login-input">
          <input type="password" placeholder="PW" class="login-input">
          <button class="login-submit-btn">로그인</button>
          
          <div class="login-footer">
            <div class="google-btn">
              <span class="google-icon">
                <img src="@/assets/logo_google.png" alt="Google Logo" class="google-logo-img">
              </span> 구글 계정 로그인
            </div>
            <div class="find-join">
              <span @click="$router.push('/find-account')">찾기</span> |
              <span class="join-link" @click="$router.push('/signup')">회원가입</span>
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
          <div v-for="pick in picks" :key="pick.title" class="pick-card">
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
      &copy; 2025 — MoneyBean Team. All rights reserved.
    </footer>
  </div>
</template>

<script>
export default {
  data: () => ({
    currentSlide: 0,
    slideInterval: null,
    menus: [
      { title: '내 자산 보기', subs: ['내 자산 입력하기', '내 자산 한눈에 보기', 'AI 진단·추천받기'] },
      { title: '예·적금', subs: ['예금', '적금'] },
      { title: '금/은/달러', subs: ['국내 시세', '해외 시세'] },
      { title: '게시판', subs: ['자유게시판', '금융정보(꿀팁)', '금융기사'] },
      { title: '기타 편의', subs: ['주변은행찾기', '유튜브 찾기', '오늘의 금전운'] },
    ],
    banners: [
      { tag: 'EVENT', title: '금융 퀴즈 챌린지!', desc: '매일 퀴즈 풀고 자산 나무에 물을 주세요.' },
      { tag: 'NEWS', title: '금리 인상 소식', desc: '나에게 유리한 예적금 상품을 찾아보세요.' },
      { tag: 'QUIZ', title: '자산 관리 MBTI', desc: '당신의 투자 성향은 어떤 콩인가요?' },
    ],
    picks: [
      { title: '카드', icon: '💳' },
      { title: '예금', icon: '🐷' },
      { title: '적금', icon: '🏦' },
      { title: '투자', icon: '📈' },
    ]
  }),
  mounted() {
    this.startSlide();
  },
  beforeUnmount() {
    clearInterval(this.slideInterval);
  },
  methods: {
    startSlide() {
      this.slideInterval = setInterval(() => {
        this.currentSlide = (this.currentSlide + 1) % this.banners.length;
      }, 4000);
    }
  }
};
</script>

<style scoped>
.moneybean-container { background-color: #f8faf9; min-height: 100vh; color: #333; }
.content-wrapper { max-width: 1100px; margin: 0 auto; padding: 40px 20px; }

/* Navbar 스타일 */
.navbar { background: white; border-bottom: 1px solid #eee; height: 80px; position: sticky; top: 0; z-index: 100; }
.nav-content { max-width: 1100px; margin: 0 auto; display: flex; align-items: center; height: 100%; padding: 0 20px; }
.logo-area { display: flex; align-items: center; cursor: pointer; margin-right: 50px; }
.bean-logo { width: 60px; height: 60px; border-radius: 50%; object-fit: cover; margin-right: 15px; }
.logo-text { font-size: 24px; font-weight: bold; color: #00a651; }

.menu-list { display: flex; gap: 20px; height: 100%; }
.menu-item { position: relative; height: 100%; display: flex; align-items: center; }
.menu-btn { background: none; border: none; font-size: 16px; font-weight: 600; cursor: pointer; padding: 10px; }

.submenu {
  display: none; position: absolute; top: 70px; left: 0; 
  background: white; border: 1px solid #eee; list-style: none;
  padding: 10px 0; width: 160px; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  border-radius: 8px;
}
.menu-item:hover .submenu { display: block; }
.submenu li { padding: 10px 20px; font-size: 14px; cursor: pointer; }
.submenu li:hover { background: #f1fcf4; color: #00a651; }

/* 배너 슬라이드 */
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

/* 로그인 박스 */
.login-box { 
  background: white; border: 1px solid #eee; border-radius: 20px; padding: 30px;
  display: flex; flex-direction: column;
}
.login-input { padding: 12px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 8px; }
.login-submit-btn { 
  background: #00a651; color: white; border: none; padding: 14px; 
  border-radius: 8px; font-weight: bold; cursor: pointer; margin-bottom: 15px;
}
.login-footer { display: flex; flex-direction: column; gap: 15px; align-items: center; font-size: 13px; }
.google-btn { cursor: pointer; color: #666; display: flex; align-items: center; gap: 5px; }
.google-btn:hover { background-color: #f5f5f5; }
.google-icon { display: flex; align-items: center; }
.google-logo-img { width: 15px; height: 15px; }
.find-join { color: #999; }
.join-link { color: #00a651; font-weight: bold; cursor: pointer; margin-left: 5px; }

/* 머니빈 Pick! */
.pick-section { margin-top: 60px; }
.section-title-container { display: flex; align-items: center; margin-bottom: 20px; gap: 10px; }
.section-logo { width: 30px; height: 30px; border-radius: 50%; object-fit: cover;}
.section-title { font-size: 22px; margin: 0; }

.pick-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.pick-card { 
  background: white; border: 1px solid #eee; border-radius: 20px; padding: 30px;
  text-align: center; cursor: pointer; transition: 0.3s;
}
.pick-card:hover { transform: translateY(-5px); border-color: #00a651; }
.pick-icon { font-size: 30px; margin-bottom: 10px; }

/* 게시판 */
.board-section { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 60px; }
.board-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 15px; }
.board-list { list-style: none; padding: 0; background: white; border-radius: 15px; border: 1px solid #eee; }
.board-list li { padding: 15px 20px; border-bottom: 1px solid #f5f5f5; font-size: 14px; cursor: pointer; }
.board-list li:hover { background: #fafafa; color: #00a651; }

.main-footer { text-align: center; padding: 40px; color: #999; font-size: 12px; }
</style>