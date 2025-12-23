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

        <button 
          class="refresh-btn" 
          @click="refreshData" 
          :disabled="isLoading"
          title="최신 금리 정보 가져오기"
        >
          🔄
        </button>
      </div>

      <div class="list-header">
        <span class="count-text">
          총 <strong>{{ filteredProducts.length }}</strong>개 상품
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

const selectedTerm = ref(12);
const isFirstSectorOnly = ref(true);
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

// 필터링 및 정렬
const filteredProducts = computed(() => {
  let products = activeTab.value === 'deposit' 
    ? (store.depositProducts || []) 
    : (store.savingProducts || []);
  
  // 1금융권 필터 (정확한 매칭)
  if (isFirstSectorOnly.value) {
    products = products.filter(p => firstSectorBanks.includes(p.kor_co_nm));
  }
  
  if (isNonFaceToFace.value) {
    products = products.filter(p => 
      p.join_way && (p.join_way.includes('인터넷') || p.join_way.includes('스마트폰'))
    );
  }

  if (selectedTerm.value !== 0) {
    products = products.filter(p => {
      return p.options && p.options.some(opt => opt.save_trm == selectedTerm.value);
    });
  }
  
  // 금리 높은 순 정렬
  return products.slice().sort((a, b) => {
     const maxRateA = Math.max(...(a.options?.map(o => o.intr_rate2) || [0]));
     const maxRateB = Math.max(...(b.options?.map(o => o.intr_rate2) || [0]));
     return maxRateB - maxRateA; 
  });
});

const goToDetail = (id, type = null) => {
  const tabType = type || activeTab.value;
  const routeName = tabType === 'deposit' ? 'deposit-detail' : 'saving-detail';
  router.push({ name: routeName, params: { id: id }, query: { from: activeTab.value } });
};
</script>

<style scoped>
.main-content { max-width: 800px; margin: 0 auto; padding: 40px 20px; }
.page-title { font-size: 24px; font-weight: 700; margin-bottom: 8px; }
.page-subtitle { color: #666; font-size: 14px; margin-bottom: 30px; }

.tab-menu { display: flex; gap: 20px; border-bottom: 1px solid #eee; margin-bottom: 25px; }
.tab-btn { background: none; border: none; padding: 10px 4px; font-size: 18px; font-weight: 600; color: #aaa; cursor: pointer; position: relative; }
.tab-btn.active { color: #333; }
.tab-btn.active::after { content: ''; position: absolute; bottom: -1px; left: 0; width: 100%; height: 3px; background-color: #00a651; }

.tab-btn.my-products { display: flex; align-items: center; gap: 6px; }
.my-count { 
  background-color: #00a651; 
  color: white; 
  font-size: 12px; 
  padding: 2px 8px; 
  border-radius: 10px; 
}

.filter-section { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; margin-bottom: 20px; padding: 15px; background-color: #f9fbfb; border-radius: 12px; }
.filter-group { display: flex; align-items: center; gap: 8px; margin-right: 10px; }
.filter-group label { font-size: 13px; font-weight: 600; color: #333; }
.term-select { padding: 8px 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; cursor: pointer; outline: none; }
.term-select:focus { border-color: #00a651; }
.filter-chip { background: white; border: 1px solid #ddd; padding: 8px 14px; border-radius: 20px; font-size: 13px; color: #555; cursor: pointer; transition: all 0.2s; }
.filter-chip.active { background-color: #e5faf0; border-color: #00a651; color: #00a651; font-weight: 600; }

.refresh-btn { 
  margin-left: auto; 
  background: none; 
  border: 1px solid #ddd; 
  border-radius: 50%; 
  width: 32px; 
  height: 32px; 
  cursor: pointer; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  transition: all 0.1s ease;
}
.refresh-btn:hover { background-color: #f0f0f0; border-color: #ccc; }
.refresh-btn:active { transform: scale(0.92); background-color: #e0e0e0; }

.list-header { display: flex; justify-content: flex-end; margin-bottom: 10px; }
.count-text { font-size: 13px; color: #888; }
.loading-state, .empty-state { text-align: center; padding: 60px 0; color: #888; }

.refresh-link { color: #00a651; font-weight: 600; cursor: pointer; text-decoration: underline; margin: 0 4px; }
.refresh-link:hover { color: #008541; }

.skeleton-container { display: flex; flex-direction: column; }
.skeleton-item { display: flex; justify-content: space-between; align-items: center; padding: 24px 10px; border-bottom: 1px solid #f0f0f0; }
.sk-left { display: flex; align-items: center; gap: 16px; flex: 1; }
.sk-info { display: flex; flex-direction: column; justify-content: center; }
.sk-right { display: flex; flex-direction: column; align-items: flex-end; }

/* 내 가입상품 탭 스타일 */
.my-products-section { margin-top: 20px; }
.my-section { margin-bottom: 40px; }
.section-title { font-size: 18px; font-weight: 600; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #00a651; }
.empty-my { text-align: center; padding: 40px; color: #888; background: #f9f9f9; border-radius: 12px; }

.login-required { text-align: center; padding: 80px 20px; }
.login-required p { color: #666; margin-bottom: 20px; }
.login-btn { background: #00a651; color: white; border: none; padding: 12px 30px; border-radius: 25px; font-size: 16px; font-weight: 600; cursor: pointer; }
.login-btn:hover { background: #008541; }
</style>