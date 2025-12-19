<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-logo" @click="$router.push('/')">
        <img src="@/assets/logo_moneybean.png" alt="로고">
        <h1>머니빈</h1>
      </div>

      <div class="login-form">
        <div class="input-group">
          <input type="text" v-model="userId" placeholder="아이디" class="input-field">
          <input type="password" v-model="userPw" placeholder="비밀번호" class="input-field">
        </div>

        <div class="login-options">
          <label class="keep-login">
            <input type="checkbox"> 로그인 상태 유지
          </label>
        </div>

        <button class="submit-btn" @click="handleLogin">로그인</button>
      </div>

      <div class="social-login">
        <div class="google-login-btn">
          <img src="@/assets/logo_google.png" alt="구글">
          구글 계정으로 로그인
        </div>
      </div>

      <div class="footer-links">
        <span @click="$router.push('/find-account')">비밀번호 찾기</span>
        <span @click="$router.push('/find-account')">아이디 찾기</span>
        <span @click="$router.push('/signup')">회원가입</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userId: '',
      userPw: ''
    }
  },
  methods: {
    handleLogin() {
      if(!this.userId || !this.userPw) {
        alert('아이디와 비밀번호를 입력해주세요.');
        return;
      }
      console.log('로그인 시도:', this.userId);
    }
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f6f7;
}
.login-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
}
.login-logo {
  text-align: center;
  margin-bottom: 30px;
  cursor: pointer;
}
.login-logo img { width: 80px; height: 80px; border-radius: 50%; object-fit: cover;}
.login-logo h1 { color: #00a651; font-size: 28px; margin-top: 10px; }

.login-form {
  background: white;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.input-group {
  border: 1px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 15px;
}
.input-field {
  width: 100%;
  padding: 15px;
  border: none;
  outline: none;
  font-size: 15px;
}
.input-field:first-child { border-bottom: 1px solid #ddd; }

.login-options {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #666;
  margin-bottom: 20px;
}
.submit-btn {
  width: 100%;
  padding: 15px;
  background: #00a651;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
}

.social-login { margin-top: 20px; }
.google-login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  font-size: 14px;
}
.google-login-btn img { width: 18px; }

.footer-links {
  margin-top: 30px;
  text-align: center;
  font-size: 13px;
  color: #888;
}
.footer-links span {
  cursor: pointer;
  margin: 0 10px;
}
.footer-links span:hover { text-decoration: underline; }
</style>