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
@import url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/GmarketSansMedium.css');

* { 
  font-family: 'GmarketSansMedium', sans-serif; 
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

button { 
  -webkit-tap-highlight-color: transparent; 
  font-family: 'GmarketSansMedium', sans-serif; 
}
</style>