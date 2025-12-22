<template>
  <div class="asset-container">
    <h1>💰 내 자산 관리</h1>

    <div v-if="!store.isDataExists" class="empty-state">
      <div class="mascot-placeholder">
        (여기에 머니빈 마스코트가 들어갈 예정)
      </div>
      <p>아직 등록된 자산이 없네요!</p>
      <p>내 자산을 입력하면 한눈에 볼 수 있어요.</p>
      <button class="primary-btn">내 자산 입력하러 가기</button>
    </div>

    <div v-else class="dashboard">
      <div class="summary-card">
        <h3>현재 총 자산</h3>
        <p class="total-amount">{{ store.totalValue.toLocaleString() }}원</p>
      </div>

      <ul class="asset-list">
        <li v-for="asset in store.assets" :key="asset.id" class="asset-item">
          <span class="category-badge">{{ asset.category_name }}</span>
          <span class="asset-name">{{ asset.name }}</span>
          <span class="asset-value">{{ Number(asset.current_value).toLocaleString() }}원</span>
        </li>
      </ul>

      <div class="ai-section">
        <button class="ai-btn">🤖 AI에게 자산진단 받기</button>
      </div>
    </div>
  </div>
</template>

<script setup>

import { onMounted } from 'vue'
import { useAssetStore } from '@/stores/assetStore'
import { useRouter } from 'vue-router' // 1. 라우터 import

const store = useAssetStore()
const router = useRouter() // 2. 라우터 사용 설정

onMounted(async () => {
  // 3. 데이터를 불러오고 결과를 변수에 담습니다.
  const result = await store.getAssets()
  
  // 4. 토큰이 없거나 인증 에러가 나면 로그인 페이지로 이동
  if (result === 'NO_TOKEN' || result === 'AUTH_ERROR') {
    window.alert('로그인이 필요한 서비스입니다.')
    
    // 중요: 본인의 로그인 라우터 이름(name)을 확인해서 넣어주세요!
    // 보통 'login' 또는 'LogInView' 등으로 되어 있을 겁니다.
    router.push({ name: 'LogInView' }) 
  }
})

</script>

<style scoped>
.asset-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.empty-state {
  margin-top: 50px;
  padding: 40px;
  background-color: #f9f9f9;
  border-radius: 15px;
}

.mascot-placeholder {
  width: 100px;
  height: 100px;
  background-color: #ddd;
  border-radius: 50%;
  margin: 0 auto 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #666;
}

.primary-btn {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}

.summary-card {
  background-color: #e8f5e9;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.total-amount {
  font-size: 24px;
  font-weight: bold;
  color: #2e7d32;
}

.asset-list {
  list-style: none;
  padding: 0;
  text-align: left;
}

.asset-item {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.category-badge {
  background-color: #eee;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-right: 10px;
}

.ai-btn {
  width: 100%;
  padding: 15px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  margin-top: 20px;
  cursor: pointer;
}

</style>