<template>
  <main class="main-content">
    <div class="page-header">
      <h2 class="page-title">예적금 비교</h2>
      <p class="page-subtitle">나에게 딱 맞는 상품을 찾아보세요.</p>
    </div>

    <div class="tab-menu">
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'deposit' }"
        @click="activeTab = 'deposit'"
      >
        예금
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'saving' }"
        @click="activeTab = 'saving'"
      >
        적금
      </button>
    </div>

    <div class="filter-section">
      <div class="filter-group">
        <label>저축 기간</label>
        <select v-model="selectedTerm" class="term-select">
          <option :value="0">전체 기간</option>
          <option :value="6">6개월</option>
          <option :value="12">12개월</option>
          <option :value="24">24개월</option>
          <option :value="36">36개월</option>
        </select>
      </div>

      <button 
        class="filter-chip" 
        :class="{ active: isFirstSectorOnly }"
        @click="isFirstSectorOnly = !isFirstSectorOnly"
      >
        1금융권
      </button>

      <button 
        class="filter-chip" 
        :class="{ active: isNonFaceToFace }"
        @click="isNonFaceToFace = !isNonFaceToFace"
      >
        방문없이 가입
      </button>
    </div>

    <div class="list-header">
       <span class="count-text">
        총 <strong>{{ filteredProducts.length }}</strong>개 상품
      </span>
    </div>

    <div class="product-list">
      <div v-if="isLoading" class="loading-state">
        데이터를 불러오는 중입니다...
      </div>

      <template v-else>
        <ProductListItem
          v-for="product in filteredProducts"
          :key="product.fin_prdt_cd"
          :product="product"
          @click="goToDetail(product.fin_prdt_cd)"
        />
        
        <div v-if="filteredProducts.length === 0" class="empty-state">
          조건에 맞는 상품이 없습니다.<br>
          필터 조건을 변경해보세요.
        </div>
      </template>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useDepositStore } from '@/stores/deposit';
import ProductListItem from '@/components/product/ProductListItem.vue';

const router = useRouter();
const store = useDepositStore();

// 상태 관리
const activeTab = ref('deposit');
const isLoading = ref(false);

// 필터 상태
const selectedTerm = ref(12); // 기본값 12개월 (가장 일반적)
const isFirstSectorOnly = ref(true); // 기본값 1금융권만 보기 (UX상 추천)
const isNonFaceToFace = ref(false); // 비대면 가입 여부

// 1금융권 목록
const majorBanks = [
  'iM뱅크', 'SC제일은행', '경남은행', '광주은행', '국민은행', 
  '기업은행', '농협은행', '부산은행', '수협은행', 
  '신한은행', '씨티은행', '우리은행', '우체국', '전북은행',
  '제주은행', '카카오뱅크', '케이뱅크', '토스뱅크', '하나은행', '한국산업은행'
];

const fetchData = async () => {
  isLoading.value = true;
  try {
    if (activeTab.value === 'deposit') {
      await store.getDepositProducts();
    } else {
      // 적금 구현 시 주석 해제
      // await store.getSavingProducts(); 
    }
  } finally {
    isLoading.value = false;
  }
};

watch(activeTab, fetchData);
onMounted(fetchData);

// 필터링 로직 (핵심)
const filteredProducts = computed(() => {
  let products = store.depositProducts || [];
  
  // 1. 1금융권 필터
  if (isFirstSectorOnly.value) {
    products = products.filter(p => majorBanks.includes(p.kor_co_nm));
  }

  // 2. 비대면 가입 필터 ('인터넷' or '스마트폰' 포함 여부)
  if (isNonFaceToFace.value) {
    products = products.filter(p => 
      p.join_way && (p.join_way.includes('인터넷') || p.join_way.includes('스마트폰'))
    );
  }

  // 3. 저축 기간 필터
  // 선택된 기간(예: 12개월) 옵션이 있는 상품만 남김
  if (selectedTerm.value !== 0) {
    products = products.filter(p => {
      // options 배열 안에 save_trm이 selectedTerm과 일치하는 항목이 하나라도 있으면 통과
      return p.options && p.options.some(opt => opt.save_trm == selectedTerm.value);
    });
  }

  return products;
});

const goToDetail = (id) => {
  router.push({ name: 'deposit-detail', params: { id: id } });
};
</script>

<style scoped>
.main-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
}

.page-subtitle {
  color: #666;
  font-size: 14px;
  margin-bottom: 30px;
}

/* 탭 메뉴 */
.tab-menu {
  display: flex;
  gap: 20px;
  border-bottom: 1px solid #eee;
  margin-bottom: 25px;
}

.tab-btn {
  background: none;
  border: none;
  padding: 10px 4px;
  font-size: 18px;
  font-weight: 600;
  color: #aaa;
  cursor: pointer;
  position: relative;
}

.tab-btn.active { color: #333; }
.tab-btn.active::after {
  content: ''; position: absolute; bottom: -1px; left: 0; width: 100%; height: 3px; background-color: #00a651;
}

/* 필터 섹션 */
.filter-section {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f9fbfb; /* 연한 배경 */
  border-radius: 12px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-right: 10px;
}

.filter-group label {
  font-size: 13px;
  font-weight: 600;
  color: #333;
}

.term-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  outline: none;
}

.term-select:focus { border-color: #00a651; }

.filter-chip {
  background: white;
  border: 1px solid #ddd;
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 13px;
  color: #555;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-chip.active {
  background-color: #e5faf0;
  border-color: #00a651;
  color: #00a651;
  font-weight: 600;
}

.list-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}

.count-text { font-size: 13px; color: #888; }

.loading-state, .empty-state {
  text-align: center; padding: 60px 0; color: #888;
}
</style>