<template>
  <div class="signup-page">
    <div class="signup-card">
      <h1>Money Bean</h1>
      <p class="subtitle">새로운 자산 관리의 시작</p>
      
      <SignupForm @success="handleSignupSuccess" />
      
      <div class="login-link">
        이미 계정이 있으신가요? 
        <RouterLink to="/login">로그인</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import SignupForm from '@/components/SignupForm.vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const handleSignupSuccess = () => {
  const isWantInput = window.confirm('회원가입을 환영합니다! 🎉\n바로 "내 자산"을 입력하시겠습니까?');

  if (isWantInput) {
    router.push({ name: 'asset-create' });
  } else {
    router.push({ name: 'home' });
  }
};
</script>

<style scoped>
.signup-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f5f7fa;
}

.signup-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h1 { margin-bottom: 5px; color: #2c3e50; }
.subtitle { color: #666; margin-bottom: 30px; font-size: 14px; }

.login-link {
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}
.login-link a {
  color: #4CAF50;
  text-decoration: none;
  font-weight: bold;
}
</style>