<template>
  <div class="bank-logo">
    <img 
      v-if="logoSrc" 
      :src="logoSrc" 
      :alt="bankName" 
      class="logo-img"
      @error="handleImageError"
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
const imageError = ref(false);

// API 은행명 → 파일명 매핑
const bankNameMap = {
  'NH농협은행': { file: '농협은행', ext: 'jpg' },
  '농협은행주식회사': { file: '농협은행', ext: 'jpg' },
  'iM뱅크': { file: 'iM뱅크', ext: 'png' },
  'SC제일은행': { file: 'SC제일은행', ext: 'png' },
  '한국스탠다드차타드은행': { file: 'SC제일은행', ext: 'png' },
  '경남은행': { file: '경남은행', ext: 'png' },
  '광주은행': { file: '광주은행', ext: 'png' },
  '국민은행': { file: '국민은행', ext: 'png' },
  'KB국민은행': { file: '국민은행', ext: 'png' },
  '기업은행': { file: '기업은행', ext: 'png' },
  'IBK기업은행': { file: '기업은행', ext: 'png' },
  '농협은행': { file: '농협은행', ext: 'jpg' },
  '부산은행': { file: '부산은행', ext: 'png' },
  'BNK부산은행': { file: '부산은행', ext: 'png' },
  '수협은행': { file: '수협은행', ext: 'png' },
  'Sh수협은행': { file: '수협은행', ext: 'png' },
  '신한은행': { file: '신한은행', ext: 'png' },
  '씨티은행': { file: '씨티은행', ext: 'png' },
  '한국씨티은행': { file: '씨티은행', ext: 'png' },
  '우리은행': { file: '우리은행', ext: 'png' },
  '우체국': { file: '우체국', ext: 'png' },
  '우체국예금보험': { file: '우체국', ext: 'png' },
  '전북은행': { file: '전북은행', ext: 'png' },
  'JB전북은행': { file: '전북은행', ext: 'png' },
  '제주은행': { file: '제주은행', ext: 'png' },
  '신한제주은행': { file: '제주은행', ext: 'png' },
  '카카오뱅크': { file: '카카오뱅크', ext: 'png' },
  '케이뱅크': { file: '케이뱅크', ext: 'png' },
  '토스뱅크': { file: '토스뱅크', ext: 'png' },
  '하나은행': { file: '하나은행', ext: 'png' },
  '한국산업은행': { file: '한국산업은행', ext: 'png' },
  'KDB산업은행': { file: '한국산업은행', ext: 'png' },
  '대구은행': { file: 'iM뱅크', ext: 'png' },
  'DGB대구은행': { file: 'iM뱅크', ext: 'png' },
  'BNK경남은행': { file: '경남은행', ext: 'png' },
};

watchEffect(() => {
  imageError.value = false;
  const mapped = bankNameMap[props.bankName];
  
  if (mapped) {
    logoSrc.value = new URL(`/src/assets/bank_logos/${mapped.file}.${mapped.ext}`, import.meta.url).href;
  } else {
    logoSrc.value = null;
  }
});

const handleImageError = () => {
  imageError.value = true;
  logoSrc.value = null;
};

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