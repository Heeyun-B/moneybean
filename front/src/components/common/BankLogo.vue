<template>
  <div class="bank-logo">
    <img 
      v-if="logoSrc" 
      :src="logoSrc" 
      :alt="bankName" 
      class="logo-img"
    />
    
    <div v-else class="logo-text" :style="{ backgroundColor: randomColor }">
      {{ bankName.charAt(0) }}
    </div>
  </div>
</template>

<script setup>
import { ref, watchEffect, computed } from 'vue';

const props = defineProps({
  bankName: {
    type: String,
    required: true
  }
});

const logoSrc = ref(null);

// 1금융권 은행 목록 (파일명과 일치해야 함)
const majorBanks = [
  'iM뱅크', 'SC제일은행', '경남은행', '광주은행', '국민은행', 
  '기업은행', '농협은행', '부산은행', '수협은행', 
  '신한은행', '씨티은행', '우리은행', '우체국', '전북은행',
  '제주은행', '카카오뱅크', '케이뱅크', '토스뱅크', '하나은행', '한국산업은행'
];

watchEffect(() => {
  if (majorBanks.includes(props.bankName)) {
    logoSrc.value = new URL(`/src/assets/bank_logos/${props.bankName}.png`, import.meta.url).href;
  } else {
    logoSrc.value = null;
  }
});

const randomColor = computed(() => {
  const colors = ['#FFD1DC', '#D1F2EB', '#D6EAF8', '#FCF3CF', '#E8DAEF'];
  const index = props.bankName.length % colors.length;
  return colors[index];
});
</script>

<style scoped>
.bank-logo {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  overflow: hidden;
  background-color: #fff;
}

.logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.logo-text {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #555;
  font-size: 14px;
}
</style>