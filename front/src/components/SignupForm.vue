<template>
  <div class="form-wrapper">
    <form @submit.prevent="submitForm">
      
      <div class="form-item">
        <label for="username">아이디 <span class="required">*</span></label>
        <div class="input-group">
          <input 
            type="text" 
            id="username" 
            v-model="form.username" 
            @input="resetIdCheck"
            placeholder="아이디를 입력하세요"
            :class="{ 'error-border': errors.username }"
          />
          <button type="button" @click="checkIdDuplicate" class="check-btn">중복확인</button>
        </div>
        <p v-if="errors.username" class="msg error">{{ errors.username }}</p>
        <p v-if="checks.username" class="msg success">사용 가능한 아이디입니다.</p>
      </div>

      <div class="form-item">
        <label for="password">비밀번호 <span class="required">*</span></label>
        <input 
          type="password" 
          id="password" 
          v-model="form.password" 
          placeholder="비밀번호를 입력하세요"
          :class="{ 'error-border': errors.password }"
        />
        <p v-if="errors.password" class="msg error">{{ errors.password }}</p>
      </div>

      <div class="form-item">
        <label for="passwordConfirm">비밀번호 확인 <span class="required">*</span></label>
        <input 
          type="password" 
          id="passwordConfirm" 
          v-model="form.passwordConfirm" 
          placeholder="비밀번호를 한 번 더 입력하세요"
          :class="{ 'error-border': errors.passwordConfirm }"
        />
        <p v-if="errors.passwordConfirm" class="msg error">{{ errors.passwordConfirm }}</p>
      </div>

      <div class="form-item">
        <label for="nickname">닉네임 <span class="required">*</span></label>
        <div class="input-group">
          <input 
            type="text" 
            id="nickname" 
            v-model="form.nickname" 
            @input="resetNicknameCheck"
            placeholder="닉네임을 입력하세요"
            :class="{ 'error-border': errors.nickname }"
          />
          <button type="button" @click="checkNicknameDuplicate" class="check-btn">중복확인</button>
        </div>
        <p v-if="errors.nickname" class="msg error">{{ errors.nickname }}</p>
        <p v-if="checks.nickname" class="msg success">사용 가능한 닉네임입니다.</p>
      </div>

      <div class="form-item">
        <label for="email">이메일 (선택)</label>
        <input 
          type="email" 
          id="email" 
          v-model="form.email" 
          placeholder="ex) user@example.com"
        />
      </div>

      <button type="submit" class="submit-btn">가입하기</button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';

const store = useAuthStore();
const API_URL = store.API_URL;

// 폼 데이터
const form = reactive({
  username: '',
  password: '',
  passwordConfirm: '', 
  nickname: '',
  email: ''
});

const errors = reactive({
  username: '',
  password: '',
  passwordConfirm: '',
  nickname: ''
});

const checks = reactive({
  username: false,
  nickname: false
});

// 초기화 로직 (입력값이 변하면 다시 검사받게 함)
const resetIdCheck = () => {
  checks.username = false;
  errors.username = '';
};
const resetNicknameCheck = () => {
  checks.nickname = false;
  errors.nickname = '';
};

const checkIdDuplicate = () => {
  if (!form.username) {
    errors.username = '아이디를 입력해주세요.';
    return;
  }
  
  // 백엔드로 요청 보내기
  axios.get(`${API_URL}/api/accounts/check-id/${form.username}/`)
    .then((res) => {
      if (res.data.is_exist) {
        // DB에 존재하면 (중복)
        errors.username = '이미 사용 중인 아이디입니다.';
        checks.username = false;
      } else {
        // DB에 없으면 (사용 가능)
        errors.username = '';
        checks.username = true;
      }
    })
    .catch((err) => {
      console.error(err);
      errors.username = '중복 확인 중 오류가 발생했습니다.';
    });
};

const checkNicknameDuplicate = () => {
  if (!form.nickname) {
    errors.nickname = '닉네임을 입력해주세요.';
    return;
  }

  // 백엔드로 요청 보내기
  axios.get(`${API_URL}/api/accounts/check-nickname/${form.nickname}/`)
    .then((res) => {
      if (res.data.is_exist) {
        errors.nickname = '이미 사용 중인 닉네임입니다.';
        checks.nickname = false;
      } else {
        errors.nickname = '';
        checks.nickname = true;
      }
    })
    .catch((err) => {
      console.error(err);
      errors.nickname = '중복 확인 중 오류가 발생했습니다.';
    });
};

// 회원가입 제출
const submitForm = () => {
  errors.username = '';
  errors.password = '';
  errors.passwordConfirm = '';
  errors.nickname = '';

  let isValid = true;

  if (!form.username) { errors.username = '필수 입력값입니다.'; isValid = false; }
  if (!form.password) { errors.password = '필수 입력값입니다.'; isValid = false; }
  if (!form.passwordConfirm) { errors.passwordConfirm = '필수 입력값입니다.'; isValid = false; }
  if (!form.nickname) { errors.nickname = '필수 입력값입니다.'; isValid = false; }

  if (form.password && form.passwordConfirm && form.password !== form.passwordConfirm) {
    errors.passwordConfirm = '비밀번호가 일치하지 않습니다.';
    isValid = false;
  }

  if (form.username && !checks.username) {
    errors.username = '아이디 중복 확인을 해주세요.';
    isValid = false;
  }
  if (form.nickname && !checks.nickname) {
    errors.nickname = '닉네임 중복 확인을 해주세요.';
    isValid = false;
  }

  if (!isValid) return;

  const payload = {
    username: form.username,
    password: form.password,
    password2: form.passwordConfirm,
    nickname: form.nickname,
    email: form.email
  };
  
  store.signUp(payload);
};
</script>

<style scoped>
.form-wrapper { width: 100%; max-width: 400px; margin: 0 auto; }
.form-item { margin-bottom: 20px; text-align: left; }
label { display: block; margin-bottom: 6px; font-size: 14px; font-weight: 600; color: #333; }
.required { color: #ff4d4f; margin-left: 4px; }
.input-group { display: flex; gap: 8px; }
input { width: 100%; padding: 10px 12px; font-size: 14px; border: 1px solid #d9d9d9; border-radius: 6px; box-sizing: border-box; }
input:focus { outline: none; border-color: #4CAF50; }
.error-border { border-color: #ff4d4f !important; }
.check-btn { white-space: nowrap; padding: 0 16px; background-color: #f0f0f0; border: 1px solid #d9d9d9; border-radius: 6px; font-size: 13px; cursor: pointer; }
.check-btn:hover { background-color: #e6e6e6; }
.msg { font-size: 12px; margin-top: 6px; margin-bottom: 0; }
.error { color: #ff4d4f; }
.success { color: #1890ff; }
.submit-btn { width: 100%; padding: 12px; background-color: #4CAF50; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: 700; cursor: pointer; margin-top: 10px; }
.submit-btn:hover { background-color: #45a049; }
</style>