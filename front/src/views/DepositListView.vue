<template>
  <main class="main-content">
    <div class="page-header">
      <h2 class="page-title">정기예금 상품 비교</h2>
      <p class="page-subtitle">실시간 금융권 데이터를 기반으로 최고 금리를 확인하세요.</p>
    </div>

    <div class="admin-section" v-if="authStore.token">
      <button @click="fetchNewData" class="update-btn">🔄 금융 데이터 업데이트</button>
      <p class="admin-tip">* 목록이 비어있다면 위 버튼을 눌러 DB에 데이터를 채워주세요.</p>
    </div>

    <div class="filter-section">
      <select v-model="selectedBank" @change="onBankChange" class="bank-select">
        <option value="">모든 은행</option>
        <option v-for="bank in bankList" :key="bank" :value="bank">{{ bank }}</option>
      </select>
    </div>

    <div class="product-grid">
      <div 
        v-for="product in store.depositProducts" 
        :key="product.fin_prdt_cd" 
        class="product-card"
        @click="goToDetail(product.fin_prdt_cd)"
      >
        <div class="bank-name">{{ product.kor_co_nm }}</div>
        <h3 class="product-name">{{ product.fin_prdt_nm }}</h3>
        
        <div class="rate-info">
          <span class="rate-label">최고 금리</span>
          <span class="rate-value">{{ getMaxRate(product.options) }}%</span>
        </div>
        
        <div class="tags">
          <span class="tag">{{ product.join_way }}</span>
          <span class="tag" v-if="product.join_member?.includes('개인')">개인 가능</span>
        </div>
      </div>
    </div>

    <div v-if="store.depositProducts.length === 0" class="no-data">
      조회된 상품이 없습니다. 데이터를 업데이트 해주세요.
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useDepositStore } from '@/stores/deposit';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const store = useDepositStore();
const authStore = useAuthStore();
const selectedBank = ref('');

const bankList = ['우리은행', '한국스탠다드차타드은행', '부산은행', '대구은행', '광주은행', '제주은행', '전북은행', '경남은행', '중소기업은행', '한국산업은행', '국민은행', '신한은행', '농협은행주식회사', '하나은행'];

onMounted(() => {
  store.getDepositProducts();
});

const onBankChange = () => {
  store.getDepositProducts(selectedBank.value);
};

const fetchNewData = () => {
  axios({
    method: 'post',
    url: 'http://127.0.0.1:8000/api/deposits/save-deposit-products/',
    headers: {
      Authorization: `Token ${authStore.token}`
    }
  })
  .then(() => {
    alert('데이터가 성공적으로 DB에 저장되었습니다.');
    store.getDepositProducts();
  })
  .catch((err) => {
    console.error(err);
    alert('데이터 저장 실패: ' + (err.response?.data?.detail || '서버 에러'));
  });
};

const getMaxRate = (options) => {
  if (!options || options.length === 0) return '-';
  const rates = options.map(o => o.intr_rate2 || 0);
  return Math.max(...rates).toFixed(2);
};

const goToDetail = (id) => {
  router.push({ name: 'deposit-detail', params: { id: id } });
};
</script>

<style scoped>
.main-content { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
.page-title { color: #00a651; font-size: 28px; margin-bottom: 8px; }
.page-subtitle { color: #666; margin-bottom: 30px; }

.admin-section {
  background: #fff9eb;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 30px;
  border: 1px solid #ffeeba;
  text-align: center;
}
.update-btn {
  background: #ffdda9;
  color: #333;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  margin-bottom: 10px;
}
.update-btn:hover { background: #473417; color: white; }
.admin-tip { font-size: 13px; color: #654321; }

.filter-section { margin-bottom: 25px; }
.bank-select { padding: 10px; border-radius: 8px; border: 1px solid #ddd; width: 200px; }

.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.product-card { 
  background: white; border: 1px solid #eee; border-radius: 16px; padding: 25px;
  cursor: pointer; transition: all 0.2s; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}
.product-card:hover { transform: translateY(-5px); border-color: #00a651; }

.bank-name { font-size: 14px; color: #888; margin-bottom: 5px; }
.product-name { font-size: 18px; margin-bottom: 15px; color: #333; }

.rate-info { background: #f1fcf4; padding: 10px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;}
.rate-label { font-size: 14px; color: #00a651; font-weight: 600; }
.rate-value { font-size: 20px; color: #00a651; font-weight: 700; }

.tags { display: flex; gap: 8px; }
.tag { background: #eee; font-size: 12px; padding: 4px 8px; border-radius: 4px; color: #666; }
.no-data { text-align: center; padding: 50px; color: #999; }
</style>