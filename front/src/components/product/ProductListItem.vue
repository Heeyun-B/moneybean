<template>
  <div class="product-item" @click="$emit('click')">
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
  }
});

defineEmits(['click']);

// 최고 금리 계산
const maxRate = computed(() => {
  if (!props.product.options?.length) return '-';
  const rates = props.product.options.map(o => o.intr_rate2 || 0);
  return Math.max(...rates).toFixed(2);
});

// 기본 금리 (가장 높은 기본 금리 혹은 첫 번째 옵션)
const baseRate = computed(() => {
  if (!props.product.options?.length) return '-';
  // 보통 최고 우대금리와 짝이 맞는 기본금리를 보여주거나, 가장 높은 기본금리를 보여줍니다.
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
}

.product-item:hover {
  background-color: #f9fbfb;
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