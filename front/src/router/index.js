import { createRouter, createWebHistory } from 'vue-router'

// 1. 메인 (Main)
import HomeView from '@/views/Main/HomeView.vue'

// 2. 인증 (Auth)
import SignUpView from '@/views/Auth/SignUpView.vue'
import LoginView from '@/views/Auth/LoginView.vue'

// 3. 자산 (Asset)
import AssetView from '@/views/Asset/AssetView.vue'
import AssetCreateView from '@/views/Asset/AssetCreateView.vue'

// 4. 유튜브 (Youtube)
import YoutubeMainView from '@/views/Youtube/YoutubeMainView.vue'
import SearchView from '@/views/Youtube/SearchView.vue'
import VideoDetailView from '@/views/Youtube/VideoDetailView.vue'
import LaterView from '@/views/Youtube/LaterView.vue'

// 5. 예적금 (Deposit)
import DepositListView from '@/views/Deposit/DepositListView.vue'
import DepositDetailView from '@/views/Deposit/DepositDetailView.vue'

// 6. 지도 (Map)
import MapView from '@/views/Map/MapView.vue'

// 7. 현물 상품 (Exchange)
import ExchangeView from '@/views/Gold/ExchangeView.vue'

// 8. 게시판 (Board)
import BoardListView from '@/views/Board/BoardListView.vue'
import BoardDetailView from '@/views/Board/BoardDetailView.vue'
import BoardWriteView from '@/views/Board/BoardWriteView.vue'
import BoardLikedView from '@/views/Board/BoardLikedView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
      beforeEnter: (to, from, next) => {
        const token = localStorage.getItem('token');
        if (token) {
          alert("이미 로그인 되어 있습니다.");
          next({ name: 'home' }); 
        } else {
          next();
        }
      }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      beforeEnter: (to, from, next) => {
        const token = localStorage.getItem('token');
        if (token) {
          alert("이미 로그인 되어 있습니다.");
          next({ name: 'home' }); 
        } else {
          next();
        }
      }
    },

    // 자산 관련
    {
      path: '/assets',
      name: 'assets',
      component: AssetView
    },
    {
      path: '/assets/create',
      name: 'asset-create',
      component: AssetCreateView
    },

    // 유튜브 관련
    {
      path: '/youtube',
      name: 'youtube-home',
      component: YoutubeMainView,
    },
    {
      path: '/youtube/search',
      name: 'search',
      component: SearchView,
    },
    {
      path: '/video/:id',
      name: 'video-detail',
      component: VideoDetailView,
    },
    {
      path: '/later',
      name: 'later-videos',
      component: LaterView,
    },

    // 예적금 관련
    {
      path: '/deposits',
      name: 'deposit-list',
      component: DepositListView
    },
    {
      path: '/deposits/:id',
      name: 'deposit-detail',
      component: DepositDetailView
    },

    // 지도 관련
    {
      path: '/map',
      name: 'map',
      component: MapView
    },

    // 현물 관련
    {
      path: '/exchange',
      name: 'exchange',
      component: ExchangeView
    },

    {
      path: '/saving-detail/:id',
      name: 'saving-detail',
      component: () => import('@/views/Deposit/SavingDetailView.vue')
    },

    // 퀴즈 관련
    {
      path: '/quiz',
      name: 'quiz',
      component: () => import('@/views/Quiz/QuizView.vue')
    },

    // 게시판 관련
    {
      path: '/board/:type',
      name: 'board-list',
      component: BoardListView
    },
    {
      path: '/board/:type/write',
      name: 'board-write',
      component: BoardWriteView
    },
    {
      path: '/board/:type/edit/:id',
      name: 'board-edit',
      component: BoardWriteView
    },
    {
      path: '/board/:type/:id',
      name: 'board-detail',
      component: BoardDetailView
    },
    {
      path: '/board-liked',
      name: 'board-liked',
      component: BoardLikedView
    },
  ],
})

export default router