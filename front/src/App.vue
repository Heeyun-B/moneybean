<template>
  <div id="app">
    <TheNavbar />
    
    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import TheNavbar from '@/components/common/TheNavbar.vue'
</script>

<style>
@import url('https://webfontworld.github.io/gmarket/GmarketSans.css');

* { 
  /* 지마켓 산스를 최우선으로 하되, 로딩 실패시만 기본 고딕 사용 */
  font-family: 'GmarketSans', sans-serif; 
  margin: 0; padding: 0; box-sizing: border-box; 
}

/* 모바일에서 텍스트가 너무 작아 보이지 않게 방지 */
html { -webkit-text-size-adjust: 100%; }

body { background-color: #f8faf9; color: #333; -webkit-font-smoothing: antialiased; }

/* 모바일 버튼 터치 시 생기는 하이라이트 제거 (선택사항) */
button { -webkit-tap-highlight-color: transparent; font-family: 'GmarketSans', sans-serif; }
</style>