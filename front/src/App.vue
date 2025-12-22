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
import TheNavbar from '@/components/common/TheNavbar.vue' // 경로 확인 필수!
</script>

<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
* { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }
body { background-color: #f8faf9; }
</style>