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
      <button 
        class="tab-btn my-products" 
        :class="{ active: activeTab === 'my' }"
        @click="activeTab = 'my'"
      >
        내 가입상품
        <span v-if="myProductsCount > 0" class="my-count">{{ myProductsCount }}</span>
      </button>
    </div>

    <!-- 내 가입상품 탭일 때 -->
    <template v-if="activeTab === 'my'">
      <div class="my-products-section" v-if="authStore.token">
        <div class="my-section">
          <h3 class="section-title">📥 가입한 예금 ({{ store.mySubscriptions.length }})</h3>
          <div v-if="store.mySubscriptions.length === 0" class="empty-my">
            가입한 예금 상품이 없습니다.
          </div>
          <ProductListItem
            v-for="(sub, index) in myDepositProducts"
            :key="'dep-' + sub.product"
            :product="sub.productData"
            :rank="index + 1"
            :isSubscribed="true"
            @click="goToDetail(sub.product, 'deposit')"
          />
        </div>

        <div class="my-section">
          <h3 class="section-title">💰 가입한 적금 ({{ store.mySavingSubscriptions.length }})</h3>
          <div v-if="store.mySavingSubscriptions.length === 0" class="empty-my">
            가입한 적금 상품이 없습니다.
          </div>
          <ProductListItem
            v-for="(sub, index) in mySavingProducts"
            :key="'sav-' + (sub.product?.fin_prdt_cd || index)"
            :product="sub.product"
            :rank="index + 1"
            :isSubscribed="true"
            @click="goToDetail(sub.product?.fin_prdt_cd, 'saving')"
          />
        </div>
      </div>
      <div v-else class="login-required">
        <p>로그인이 필요한 서비스입니다.</p>
        <button @click="$router.push('/login')" class="login-btn">로그인하기</button>
      </div>
    </template>

    <!-- 예금/적금 탭일 때 -->
    <template v-else>
      <!-- 검색 영역 -->
      <div class="search-section">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="상품명 또는 은행명으로 검색"
            class="search-input"
          />
          <button v-if="searchKeyword" @click="searchKeyword = ''" class="clear-btn">✕</button>
        </div>
      </div>

      <!-- 필터 영역 -->
      <div class="filter-section">
        <div class="filter-row">
          <div class="filter-group">
            <label>저축 기간</label>
            <select v-model="selectedTerm" class="filter-select">
              <option :value="0">전체 기간</option>
              <option :value="6">6개월</option>
              <option :value="12">12개월</option>
              <option :value="24">24개월</option>
              <option :value="36">36개월</option>
            </select>
          </div>

          <div class="filter-group">
            <label>은행 선택</label>
            <select v-model="selectedBank" class="filter-select">
              <option value="">전체 은행</option>
              <option v-for="bank in availableBanks" :key="bank" :value="bank">
                {{ bank }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>정렬 기준</label>
            <select v-model="sortBy" class="filter-select">
              <option value="rate_desc">금리 높은순</option>
              <option value="rate_asc">금리 낮은순</option>
              <option value="name_asc">상품명순</option>
              <option value="bank_asc">은행명순</option>
            </select>
          </div>

          <button
            class="refresh-btn"
            @click="refreshData"
            :disabled="isLoading"
            title="최신 금리 정보 가져오기"
          >
            🔄
          </button>
        </div>

        <div class="filter-chips">
          <button
            class="filter-chip"
            :class="{ active: isFirstSectorOnly }"
            @click="isFirstSectorOnly = !isFirstSectorOnly"
          >
            <span class="chip-icon">🏦</span>
            1금융권만
          </button>

          <button
            class="filter-chip"
            :class="{ active: isNonFaceToFace }"
            @click="isNonFaceToFace = !isNonFaceToFace"
          >
            <span class="chip-icon">📱</span>
            비대면 가입
          </button>

          <button
            v-if="hasActiveFilters"
            class="filter-chip reset"
            @click="resetFilters"
          >
            <span class="chip-icon">🔄</span>
            필터 초기화
          </button>
        </div>
      </div>

      <div class="list-header">
        <span class="count-text">
          총 <strong>{{ filteredProducts.length }}</strong>개 상품
        </span>
        <span v-if="hasActiveFilters" class="filter-active-text">
          (필터 적용 중)
        </span>
      </div>

      <div class="product-list">
        <div v-if="isLoading" class="skeleton-container">
          <div v-for="n in 5" :key="n" class="skeleton-item">
            <div class="sk-left">
              <SkeletonLoader width="40px" height="40px" radius="50%" />
              <div class="sk-info">
                <SkeletonLoader width="50px" height="14px" style="margin-bottom: 5px" />
                <SkeletonLoader width="150px" height="20px" />
              </div>
            </div>
            <div class="sk-right">
              <SkeletonLoader width="60px" height="14px" style="margin-bottom: 5px" />
              <SkeletonLoader width="80px" height="24px" />
            </div>
          </div>
        </div>

        <template v-else>
          <ProductListItem
            v-for="(product, index) in filteredProducts"
            :key="product.fin_prdt_cd"
            :product="product"
            :rank="index + 1"
            :isSubscribed="isProductSubscribed(product.fin_prdt_cd)"
            @click="goToDetail(product.fin_prdt_cd)"
          />
          
          <div v-if="filteredProducts.length === 0" class="empty-state">
            조건에 맞는 상품이 없습니다.<br>
            필터 조건을 변경하거나 
            <span class="refresh-link" @click="refreshData">
              '최신화'
            </span> 
            버튼을 눌러보세요.
          </div>
        </template>
      </div>
    </template>
  </main>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useDepositStore } from '@/stores/deposit';
import { useAuthStore } from '@/stores/auth';
import ProductListItem from '@/components/product/ProductListItem.vue';
import SkeletonLoader from '@/components/common/SkeletonLoader.vue';

const route = useRoute();
const router = useRouter();
const store = useDepositStore();
const authStore = useAuthStore();

const activeTab = ref('deposit');
const isLoading = ref(false);

// 필터 및 정렬 상태
const searchKeyword = ref('');
const selectedTerm = ref(0);
const selectedBank = ref('');
const sortBy = ref('rate_desc');
const isFirstSectorOnly = ref(false);
const isNonFaceToFace = ref(false);

// 1금융권 은행 목록 (정확한 매칭을 위해 수정)
const firstSectorBanks = [
  '국민은행', 'KB국민은행',
  '신한은행',
  '우리은행',
  '하나은행',
  'NH농협은행', '농협은행주식회사',
  '기업은행', 'IBK기업은행',
  '한국산업은행', 'KDB산업은행',
  '수협은행', 'Sh수협은행',
  '부산은행', 'BNK부산은행',
  '대구은행', 'DGB대구은행', 'iM뱅크',
  '경남은행', 'BNK경남은행',
  '광주은행',
  '전북은행', 'JB전북은행',
  '제주은행', '신한제주은행',
  'SC제일은행', '한국스탠다드차타드은행',
  '씨티은행', '한국씨티은행',
  '우체국', '우체국예금보험',
  '카카오뱅크',
  '케이뱅크',
  '토스뱅크'
];

// 내 가입 상품 수
const myProductsCount = computed(() => {
  return store.mySubscriptions.length + store.mySavingSubscriptions.length;
});

// 내 예금 상품 (상품 정보 포함)
const myDepositProducts = computed(() => {
  return store.mySubscriptions.map(sub => {
    const productData = store.depositProducts.find(p => p.fin_prdt_cd === sub.product);
    return {
      ...sub,
      productData: productData || {
        fin_prdt_cd: sub.product,
        kor_co_nm: sub.bank_name || '알 수 없음',
        fin_prdt_nm: sub.product_name || '상품명 없음',
        options: []
      }
    };
  });
});

// 내 적금 상품
const mySavingProducts = computed(() => {
  return store.mySavingSubscriptions;
});

// 데이터 가져오기
const fetchData = async (forceUpdate = false) => {
  if (isLoading.value) return; 
  isLoading.value = true;

  try {
    const isDeposit = activeTab.value === 'deposit';
    
    if (!forceUpdate) {
      if (isDeposit) await store.getDepositProducts();
      else await store.getSavingProducts();
    }

    const currentList = isDeposit ? store.depositProducts : store.savingProducts;

    if (forceUpdate || !currentList || currentList.length === 0) {
      console.log(`[${activeTab.value}] 최신 데이터를 가져옵니다...`);
      
      if (isDeposit) {
        await store.saveDepositProducts(); 
        await store.getDepositProducts();  
      } else {
        await store.saveSavingProducts();  
        await store.getSavingProducts();   
      }
    }

    // 로그인 상태면 가입 목록도 가져오기
    if (authStore.token) {
      await store.getMySubscriptions();
      await store.getMySavingSubscriptions();
    }
  } catch (err) {
    console.error("데이터 로딩 실패:", err);
  } finally {
    isLoading.value = false;
  }
};

const refreshData = () => {
  if (confirm('최신 데이터를 불러오시겠습니까? 시간이 조금 걸릴 수 있습니다.')) {
    fetchData(true); 
  }
};

watch(activeTab, (newTab) => {
  if (newTab === 'my') {
    // 내 가입상품 탭이면 가입 목록만 새로고침
    if (authStore.token) {
      store.getMySubscriptions();
      store.getMySavingSubscriptions();
    }
  } else {
    fetchData(false);
  }
});

onMounted(() => {
  // URL 쿼리에서 탭 상태 복원
  const tabFromQuery = route.query.tab;
  if (tabFromQuery && ['deposit', 'saving', 'my'].includes(tabFromQuery)) {
    activeTab.value = tabFromQuery;
  }
  
  if (activeTab.value !== 'my') {
    fetchData(false);
  } else if (authStore.token) {
    store.getMySubscriptions();
    store.getMySavingSubscriptions();
  }
});

// 상품 가입 여부 확인
const isProductSubscribed = (finPrdtCd) => {
  if (activeTab.value === 'deposit') {
    return store.mySubscriptions.some(sub => sub.product === finPrdtCd);
  } else {
    return store.mySavingSubscriptions.some(sub => 
      (sub.product?.fin_prdt_cd || sub.product) === finPrdtCd
    );
  }
};

// 사용 가능한 은행 목록 (1금융권만)
const availableBanks = computed(() => {
  const products = activeTab.value === 'deposit'
    ? (store.depositProducts || [])
    : (store.savingProducts || []);

  const banks = new Set(
    products
      .map(p => p.kor_co_nm)
      .filter(bank => firstSectorBanks.includes(bank))
  );

  return Array.from(banks).sort();
});

// 필터가 활성화되어 있는지 확인
const hasActiveFilters = computed(() => {
  return searchKeyword.value !== '' ||
    selectedTerm.value !== 0 ||
    selectedBank.value !== '' ||
    isFirstSectorOnly.value ||
    isNonFaceToFace.value;
});

// 필터 초기화
const resetFilters = () => {
  searchKeyword.value = '';
  selectedTerm.value = 0;
  selectedBank.value = '';
  sortBy.value = 'rate_desc';
  isFirstSectorOnly.value = false;
  isNonFaceToFace.value = false;
};

// 필터링 및 정렬
const filteredProducts = computed(() => {
  let products = activeTab.value === 'deposit'
    ? (store.depositProducts || [])
    : (store.savingProducts || []);

  // 검색 필터
  if (searchKeyword.value.trim()) {
    const keyword = searchKeyword.value.trim().toLowerCase();
    products = products.filter(p =>
      p.fin_prdt_nm?.toLowerCase().includes(keyword) ||
      p.kor_co_nm?.toLowerCase().includes(keyword)
    );
  }

  // 은행 선택 필터
  if (selectedBank.value) {
    products = products.filter(p => p.kor_co_nm === selectedBank.value);
  }

  // 1금융권 필터
  if (isFirstSectorOnly.value) {
    products = products.filter(p => firstSectorBanks.includes(p.kor_co_nm));
  }

  // 비대면 가입 필터
  if (isNonFaceToFace.value) {
    products = products.filter(p =>
      p.join_way && (p.join_way.includes('인터넷') || p.join_way.includes('스마트폰'))
    );
  }

  // 저축 기간 필터
  if (selectedTerm.value !== 0) {
    products = products.filter(p => {
      return p.options && p.options.some(opt => opt.save_trm == selectedTerm.value);
    });
  }

  // 정렬
  return products.slice().sort((a, b) => {
    switch (sortBy.value) {
      case 'rate_desc':
        const maxRateA = Math.max(...(a.options?.map(o => o.intr_rate2) || [0]));
        const maxRateB = Math.max(...(b.options?.map(o => o.intr_rate2) || [0]));
        return maxRateB - maxRateA;

      case 'rate_asc':
        const minRateA = Math.max(...(a.options?.map(o => o.intr_rate2) || [0]));
        const minRateB = Math.max(...(b.options?.map(o => o.intr_rate2) || [0]));
        return minRateA - minRateB;

      case 'name_asc':
        return (a.fin_prdt_nm || '').localeCompare(b.fin_prdt_nm || '', 'ko');

      case 'bank_asc':
        return (a.kor_co_nm || '').localeCompare(b.kor_co_nm || '', 'ko');

      default:
        return 0;
    }
  });
});

const goToDetail = (id, type = null) => {
  const tabType = type || activeTab.value;
  const routeName = tabType === 'deposit' ? 'deposit-detail' : 'saving-detail';
  router.push({ name: routeName, params: { id: id }, query: { from: activeTab.value } });
};
</script>

<style scoped>
.main-content { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
.page-title { font-size: 28px; font-weight: 700; margin-bottom: 8px; color: #222; }
.page-subtitle { color: #666; font-size: 15px; margin-bottom: 30px; }

.tab-menu { display: flex; gap: 20px; border-bottom: 2px solid #f0f0f0; margin-bottom: 30px; }
.tab-btn { background: none; border: none; padding: 12px 6px; font-size: 17px; font-weight: 600; color: #999; cursor: pointer; position: relative; transition: color 0.2s; }
.tab-btn:hover { color: #555; }
.tab-btn.active { color: #00a651; }
.tab-btn.active::after { content: ''; position: absolute; bottom: -2px; left: 0; width: 100%; height: 3px; background-color: #00a651; border-radius: 3px 3px 0 0; }

.tab-btn.my-products { display: flex; align-items: center; gap: 6px; }
.my-count {
  background-color: #00a651;
  color: white;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 700;
}

/* 검색 영역 */
.search-section { margin-bottom: 20px; }
.search-box {
  display: flex;
  align-items: center;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 12px 16px;
  transition: all 0.2s;
}
.search-box:focus-within {
  border-color: #00a651;
  box-shadow: 0 0 0 3px rgba(0, 166, 81, 0.1);
}
.search-icon {
  font-size: 18px;
  margin-right: 10px;
  color: #999;
}
.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
  color: #333;
}
.search-input::placeholder {
  color: #aaa;
}
.clear-btn {
  background: #f0f0f0;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  color: #666;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}
.clear-btn:hover {
  background: #e0e0e0;
  color: #333;
}

/* 필터 영역 */
.filter-section {
  background: linear-gradient(135deg, #f8fafb 0%, #f0f4f7 100%);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
  align-items: center;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.filter-group label {
  font-size: 12px;
  font-weight: 600;
  color: #555;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-select {
  padding: 10px 14px;
  border: 2px solid #ddd;
  border-radius: 10px;
  font-size: 14px;
  cursor: pointer;
  outline: none;
  background: white;
  color: #333;
  font-weight: 500;
  transition: all 0.2s;
  min-width: 140px;
}

.filter-select:hover {
  border-color: #bbb;
}

.filter-select:focus {
  border-color: #00a651;
  box-shadow: 0 0 0 3px rgba(0, 166, 81, 0.1);
}

.filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-chip {
  background: white;
  border: 2px solid #e0e0e0;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 13px;
  color: #555;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-chip:hover {
  border-color: #00a651;
  background: #f8fdf9;
}

.filter-chip.active {
  background: linear-gradient(135deg, #00a651 0%, #008e45 100%);
  border-color: #00a651;
  color: white;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0, 166, 81, 0.3);
}

.filter-chip.reset {
  background: #fff3e0;
  border-color: #ffb74d;
  color: #f57c00;
}

.filter-chip.reset:hover {
  background: #ffe0b2;
  border-color: #ffa726;
}

.chip-icon {
  font-size: 14px;
}

.refresh-btn {
  margin-left: auto;
  background: white;
  border: 2px solid #ddd;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  font-size: 16px;
}

.refresh-btn:hover {
  background: #f8f8f8;
  border-color: #00a651;
  transform: rotate(90deg);
}

.refresh-btn:active {
  transform: rotate(90deg) scale(0.9);
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 목록 헤더 */
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 0 4px;
}

.count-text {
  font-size: 14px;
  color: #666;
}

.count-text strong {
  color: #00a651;
  font-weight: 700;
  font-size: 16px;
}

.filter-active-text {
  font-size: 12px;
  color: #00a651;
  font-weight: 600;
  background: #e5faf0;
  padding: 4px 10px;
  border-radius: 12px;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #999;
  font-size: 15px;
  line-height: 1.6;
}

.refresh-link {
  color: #00a651;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  margin: 0 4px;
}

.refresh-link:hover {
  color: #008541;
}

.skeleton-container {
  display: flex;
  flex-direction: column;
}

.skeleton-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 10px;
  border-bottom: 1px solid #f0f0f0;
}

.sk-left {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.sk-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.sk-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

/* 내 가입상품 탭 */
.my-products-section {
  margin-top: 20px;
}

.my-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #00a651;
}

.empty-my {
  text-align: center;
  padding: 40px;
  color: #888;
  background: #f9f9f9;
  border-radius: 12px;
}

.login-required {
  text-align: center;
  padding: 80px 20px;
}

.login-required p {
  color: #666;
  margin-bottom: 20px;
}

.login-btn {
  background: #00a651;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.login-btn:hover {
  background: #008541;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3);
}

/* 반응형 */
@media (max-width: 768px) {
  .filter-row {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group {
    width: 100%;
  }

  .filter-select {
    width: 100%;
  }

  .refresh-btn {
    margin-left: 0;
    align-self: flex-end;
  }

  .filter-chips {
    justify-content: center;
  }
}
</style>