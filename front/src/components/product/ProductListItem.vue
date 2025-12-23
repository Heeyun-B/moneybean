<template>
  <div class="product-item" :class="{ subscribed: isSubscribed }" @click="$emit('click')">
    <!-- 순위 메달 -->
    <div v-if="rank && rank <= 3" class="rank-medal" :class="`rank-${rank}`">
      {{ rank === 1 ? '🥇' : rank === 2 ? '🥈' : '🥉' }}
    </div>
    <div v-else-if="rank" class="rank-number">{{ rank }}</div>

    <div class="left-section">
      <BankLogo :bankName="product.kor_co_nm" class="item-logo" />
      
      <div class="info-box">
        <span class="bank-name">{{ product.kor_co_nm }}</span>
        <h3 class="product-name">{{ product.fin_prdt_nm }}</h3>
        
        <div class="tags">
          <span class="tag" v-if="product.join_way">{{ product.join_way.split(',')[0] }}</span>
          <span class="tag highlight" v-if="product.join_way?.includes('스마트폰') || product.join_way?.includes('인터넷')">
            비대면
          </span>
          <span class="tag subscribed-tag" v-if="isSubscribed">가입중</span>
        </div>
      </div>
    </div>

    <div class="right-section">
      <div class="rate-box">
        <p class="rate-label">최고 금리</p>
        <p class="max-rate">{{ maxRate }}%</p>
      </div>
      <div class="rate-box sub">
        <p class="rate-label">기본 금리</p>
        <p class="base-rate">{{ baseRate }}%</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue';
import BankLogo from '@/components/common/BankLogo.vue';

const props = defineProps({
  product: {
    type: Object,
    required: true
  },
  rank: {
    type: Number,
    default: null
  },
  isSubscribed: {
    type: Boolean,
    default: false
  }
});

defineEmits(['click']);

// 최고 금리 계산
const maxRate = computed(() => {
  if (!props.product.options?.length) return '-';
  const rates = props.product.options.map(o => o.intr_rate2 || 0);
  return Math.max(...rates).toFixed(2);
});

// 기본 금리
const baseRate = computed(() => {
  if (!props.product.options?.length) return '-';
  const rates = props.product.options.map(o => o.intr_rate || 0);
  return Math.max(...rates).toFixed(2);
});
</script>

<style scoped>
.product-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 10px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
  position: relative;
}

.product-item:hover {
  background-color: #f9fbfb;
}

.product-item.subscribed {
  background-color: #f0fdf4;
  border-left: 3px solid #00a651;
}

/* 순위 메달 */
.rank-medal {
  font-size: 24px;
  min-width: 36px;
  text-align: center;
}

.rank-number {
  font-size: 14px;
  font-weight: 600;
  color: #888;
  min-width: 36px;
  text-align: center;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.info-box {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.bank-name {
  font-size: 13px;
  color: #888;
}

.product-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.tags {
  display: flex;
  gap: 6px;
  margin-top: 4px;
}

.tag {
  font-size: 11px;
  background-color: #f2f4f6;
  color: #4e5968;
  padding: 3px 6px;
  border-radius: 4px;
}

.tag.highlight {
  background-color: #e5faf0;
  color: #00a651;
}

.tag.subscribed-tag {
  background-color: #00a651;
  color: white;
  font-weight: 600;
}

.right-section {
  text-align: right;
  min-width: 100px;
}

.rate-box {
  margin-bottom: 4px;
}

.rate-label {
  font-size: 12px;
  color: #888;
  margin: 0;
}

.max-rate {
  font-size: 18px;
  font-weight: 700;
  color: #00a651;
  margin: 0;
}

.base-rate {
  font-size: 14px;
  color: #888;
  margin: 0;
}

</style>