<template>
  <div id="app">
    <TheNavbar />
    
    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { watch } from 'vue'
import { RouterView } from 'vue-router'
import TheNavbar from '@/components/common/TheNavbar.vue'
import { useAuthStore } from '@/stores/auth'
import { useBoardStore } from '@/stores/board'

const authStore = useAuthStore()
const boardStore = useBoardStore()

// 사용자가 변경되면 좋아요 정보 다시 로드
watch(() => authStore.userNickname, () => {
  boardStore.reloadLikedPosts()
})
</script>

<style>
/* 1. 외부 주소 대신 로컬 파일을 불러오도록 설정 */
@font-face {
  font-family: 'GmarketSans';
  src: url('./assets/fonts/GmarketSansTTFMedium.ttf') format('truetype');
  font-weight: 500;
  font-style: normal;
}

* { 
  /* 2. 폰트 적용 ( !important를 추가해서 확실히 적용되게 합니다 ) */
  font-family: 'GmarketSans', sans-serif !important; 
  margin: 0; 
  padding: 0; 
  box-sizing: border-box; 
}

html { -webkit-text-size-adjust: 100%; }

body { 
  background-color: #f8faf9; 
  color: #333; 
  -webkit-font-smoothing: antialiased; 
}

/* 버튼에도 폰트 적용 */
button { 
  -webkit-tap-highlight-color: transparent; 
  font-family: 'GmarketSans', sans-serif !important; 
}
</style>