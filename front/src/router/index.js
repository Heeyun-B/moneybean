import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LoginView from '@/views/LoginView.vue'
import AssetView from '@/views/AssetView.vue' 
import AssetCreateView from '@/views/AssetCreateView.vue'

// 유튜브 관련 뷰
import YoutubeMainView from '@/views/YoutubeMainView.vue'
import SearchView from '@/views/SearchView.vue'
import VideoDetailView from '@/views/VideoDetailView.vue'
import LaterView from '@/views/LaterView.vue'

// 예적금 관련 뷰
import DepositListView from '@/views/DepositListView.vue'
import DepositDetailView from '@/views/DepositDetailView.vue'

// 카카오맵 관련 뷰
import MapView from '@/views/MapView.vue'

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

    {
      path: '/map',
      name: 'map',
      component: MapView
    },

  ],
})

export default router