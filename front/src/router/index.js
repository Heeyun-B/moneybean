import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import AssetView from '@/views/AssetView.vue' 

// 유튜브 관련 뷰
import YoutubeMainView from '@/views/YoutubeMainView.vue'
import SearchView from '@/views/SearchView.vue'
import VideoDetailView from '@/views/VideoDetailView.vue'
import LaterView from '@/views/LaterView.vue'

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
      component: SignUpView
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView
    },
    {
      path: '/asset',
      name: 'asset',
      component: AssetView
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

  ],
})

export default router