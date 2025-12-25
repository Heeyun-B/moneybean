<template>
  <main class="main-content" v-if="depositDetail">
    <div class="detail-header">
      <button @click="goBack" class="back-btn">← 뒤로가기</button>
      <p class="bank-name">{{ depositDetail.product.kor_co_nm }}</p>
      <h2 class="product-title">{{ depositDetail.product.fin_prdt_nm }}</h2>
    </div>

    <div class="content-wrapper">
      <section class="info-section">
        <div class="info-card">
          <div class="info-item">
            <span class="label">가입 대상</span>
            <p>{{ depositDetail.product.join_member }}</p>
          </div>
          <div class="info-item">
            <span class="label">가입 방법</span>
            <p>{{ depositDetail.product.join_way }}</p>
          </div>
          <div class="info-item">
            <span class="label">우대 조건</span>
            <p class="text-block">{{ depositDetail.product.spcl_cnd || '해당 사항 없음' }}</p>
          </div>
          <div class="info-item">
            <span class="label">만기 후 이자율</span>
            <p class="text-block">{{ depositDetail.product.mtrt_int }}</p>
          </div>
        </div>
      </section>

      <section class="rate-section">
        <h3 class="sub-title">기간별 금리 안내</h3>
        <div class="table-container">
          <table class="rate-table">
            <thead>
              <tr>
                <th>저축 기간</th>
                <th>금리 유형</th>
                <th>저축 금리</th>
                <th>최고 우대금리</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="option in depositDetail.options" :key="option.id">
                <td>{{ option.save_trm }}개월</td>
                <td>{{ option.intr_rate_type_nm }}</td>
                <td>{{ option.intr_rate }}%</td>
                <td class="bold-rate">{{ option.intr_rate2 }}%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <div class="action-section" v-if="authStore.isAuthenticated">
        <button v-if="isSubscribed" @click="handleUnsubscribe" class="unsubscribe-btn">
          이 상품 가입 해제하기
        </button>
        <button v-else @click="handleSubscribe" class="subscribe-btn">
          이 상품 가입하기
        </button>
      </div>
    </div>
  </main>
  
  <div v-else class="loading">
    데이터를 불러오는 중입니다...
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useDepositStore } from '@/stores/deposit';
import { useAuthStore } from '@/stores/auth';

const route = useRoute();
const router = useRouter();
const store = useDepositStore();
const authStore = useAuthStore();

const depositDetail = computed(() => store.depositDetail);
const isSubscribed = ref(false);

// 뒤로가기 - 탭 유지
const goBack = () => {
  const fromTab = route.query.from || 'deposit';
  router.push({ name: 'deposit-list', query: { tab: fromTab } });
};

// 가입 여부 확인 로직
const checkSubscriptionStatus = async () => {
  if (authStore.token) {
    await store.getMySubscriptions(authStore.token);
    const prdtCd = route.params.id;
    
    isSubscribed.value = store.mySubscriptions.some((sub) => {
      return String(sub.product).trim() === String(prdtCd).trim();
    });
  }
};

onMounted(async () => {
  const prdtCd = route.params.id;
  await store.getDepositDetail(prdtCd);
  await checkSubscriptionStatus();
});

// 가입하기
const handleSubscribe = () => {
  if (!confirm('이 상품에 가입하시겠습니까?')) return;

  const finPrdtCd = depositDetail.value.product.fin_prdt_cd;
  const firstOptionId = depositDetail.value.options[0]?.id;

  store.subscribeProduct(finPrdtCd, firstOptionId, authStore.token)
    .then(() => {
      alert('상품 가입이 완료되었습니다!');
      isSubscribed.value = true;
    })
    .catch((err) => {
      const msg = err.response?.data?.error || '가입 중 오류가 발생했습니다.';
      alert(msg);
    });
};

// 가입 해제하기
const handleUnsubscribe = () => {
  if (!confirm('정말 가입을 해제하시겠습니까?')) return;

  const finPrdtCd = depositDetail.value.product.fin_prdt_cd;

  store.unsubscribeProduct(finPrdtCd, authStore.token)
    .then(() => {
      alert('가입 해제가 완료되었습니다.');
      isSubscribed.value = false;
    })
    .catch((err) => {
      const msg = err.response?.data?.error || '해제 중 오류가 발생했습니다.';
      alert(msg);
    });
};
</script>

<style scoped>
.main-content { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
.back-btn { background: none; border: none; color: #888; cursor: pointer; margin-bottom: 20px; }
.bank-name { color: #00a651; font-weight: 600; margin-bottom: 5px; }
.product-title { font-size: 32px; font-weight: 700; margin-bottom: 40px; }
.info-card { background: #f9f9f9; border-radius: 12px; padding: 30px; margin-bottom: 40px; }
.info-item { margin-bottom: 20px; }
.label { display: block; font-weight: 600; color: #333; margin-bottom: 8px; font-size: 15px; }
.text-block { white-space: pre-wrap; line-height: 1.6; color: #666; font-size: 14px; }
.sub-title { font-size: 20px; font-weight: 600; margin-bottom: 20px; }
.table-container { overflow-x: auto; }
.rate-table { width: 100%; border-collapse: collapse; text-align: center; }
.rate-table th { border-bottom: 2px solid #eee; padding: 15px; color: #888; font-size: 14px; }
.rate-table td { padding: 15px; border-bottom: 1px solid #f2f2f2; }
.bold-rate { color: #00a651; font-weight: 700; font-size: 18px; }
.action-section { display: flex; justify-content: center; margin-top: 50px; }
.subscribe-btn, .unsubscribe-btn { 
  border: none; padding: 15px 60px; 
  border-radius: 30px; font-size: 18px; font-weight: 600; cursor: pointer;
  transition: background 0.2s; color: white;
}
.subscribe-btn { background: #00a651; }
.subscribe-btn:hover { background: #008541; }
.unsubscribe-btn { background: #ffeed4; color: #333; }
.unsubscribe-btn:hover { background: #473417; color: white; }
.loading { text-align: center; margin-top: 100px; color: #888; }
</style>