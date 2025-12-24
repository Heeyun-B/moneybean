<template>
  <div class="loader-container">
    <div class="animation-wrapper">
      <div class="spinner"></div>
      <img src="@/assets/logo_bean.png" alt="loading" class="inner-logo">
    </div>
    <h3 class="loader-title">잠시만 기다려주세요</h3>
    <p class="loader-msg">{{ message }}</p>
    <div class="progress-track">
      <div class="progress-fill"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: { type: String, default: '데이터를 불러오는 중입니다...' }
})
</script>

<style scoped>
.loader-container { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; }
.animation-wrapper { position: relative; width: 120px; height: 120px; margin-bottom: 30px; }
.spinner {
  width: 100%; height: 100%; border: 4px solid #f0fdf4; border-top: 4px solid #00a651;
  border-radius: 50%; animation: spin 1s linear infinite;
}
.inner-logo { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 50px; }
.loader-title { font-size: 20px; font-weight: 800; color: #333; margin-bottom: 10px; }
.loader-msg { font-size: 15px; color: #666; margin-bottom: 30px; text-align: center; line-height: 1.5; }

.progress-track { width: 280px; height: 8px; background: #eee; border-radius: 10px; overflow: hidden; }
.progress-fill {
  width: 100%; height: 100%; background: linear-gradient(90deg, #00a651, #34d399);
  animation: flow 2s infinite ease-in-out; transform-origin: left;
}

@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
@keyframes flow { 0% { transform: scaleX(0); } 50% { transform: scaleX(0.6); } 100% { transform: scaleX(1); } }
</style>