<template>
  <div class="quiz-container">
    <div v-if="!quiz" class="loading-box">
      <div class="spinner"></div>
      <p>오늘의 퀴즈를 가져오는 중...</p>
    </div>
    
    <div v-else class="quiz-card">
      <div class="quiz-header">
        <span class="day-badge">오늘의 퀴즈</span>
        <h3>금융 상식 OX</h3>
      </div>

      <div v-if="hasAttended || isAnswered" class="already-done">
        <div class="question-section">
          <p class="question-text">{{ quiz.question }}</p>
        </div>
        
        <div class="result-msg">
          <div class="status-badge" v-if="hasAttended">이미 참여한 문제입니다</div>
          <h4 v-if="isAnswered" :class="isCorrect ? 'text-correct' : 'text-wrong'">
            {{ isCorrect ? '정답입니다!' : '틀렸습니다' }}
          </h4>
          
          <div class="answer-reveal">
            <span class="label">오늘의 정답</span>
            <span class="answer-char">{{ quiz.answer ? 'O' : 'X' }}</span>
          </div>

          <div class="description-box">
            <p class="description-label">💡 해설</p>
            <p class="description-text">{{ quiz.description }}</p>
          </div>
        </div>
        
        <button class="back-home-btn" @click="router.push('/')">홈으로 돌아가기</button>
      </div>

      <div v-else class="quiz-play">
        <div class="question-section">
          <p class="question-text">{{ quiz.question }}</p>
        </div>

        <div class="answer-btns">
          <button class="btn-o" @click="checkAnswer(true)">O</button>
          <button class="btn-x" @click="checkAnswer(false)">X</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const quiz = ref(null)
const isAnswered = ref(false)
const isCorrect = ref(false)
const hasAttended = ref(false)

const fetchQuiz = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get('http://127.0.0.1:8000/api/quizzes/today/', {
      headers: { Authorization: `Token ${token}` }
    })
    
    quiz.value = res.data
    
    if (res.data.has_attended) {
      hasAttended.value = true
    }
  } catch (err) {
    if (err.response?.status === 401) {
      alert('로그인이 필요한 서비스입니다.')
      router.push('/login')
    }
  }
}

const checkAnswer = async (userChoice) => {
  // 1. 즉시 화면에 정답 노출
  isAnswered.value = true
  isCorrect.value = (userChoice === quiz.value.answer)
  
  // 2. 서버에 출석(참여) 기록 전송
  try {
    const token = localStorage.getItem('token')
    await axios.post('http://127.0.0.1:8000/api/quizzes/attendance/', 
      { quiz_id: quiz.value.id }, 
      { headers: { Authorization: `Token ${token}` } }
    )
  } catch (err) {
    // 이미 풀었을 경우 400 에러가 나면 참여 완료 상태로 강제 전환
    if (err.response?.status === 400) {
      hasAttended.value = true
      console.log('이미 처리된 출석입니다.')
    }
  }
}

onMounted(fetchQuiz)
</script>

<style scoped>
/* 로딩 애니메이션 */
.loading-box { text-align: center; color: #00a651; font-weight: bold; }
.spinner { width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #00a651; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

/* 참여 완료 UI 강조 */
.status-badge { background: #f0f0f0; color: #888; padding: 6px 16px; border-radius: 20px; font-size: 13px; margin-bottom: 20px; display: inline-block; }
.answer-reveal { margin: 20px 0; padding: 15px; border-bottom: 1px solid #eee; }
.answer-reveal .label { color: #666; margin-right: 15px; }
.answer-reveal .answer-char { font-size: 32px; font-weight: 900; color: #00a651; }

.text-correct { color: #4caf50; font-size: 24px; margin-bottom: 10px; }
.text-wrong { color: #f44336; font-size: 24px; margin-bottom: 10px; }

.description-box { background: #f9fdfa; border: 1px solid #e8f5e9; padding: 20px; border-radius: 15px; text-align: left; margin-top: 20px; }
.description-label { font-weight: bold; margin-bottom: 5px; color: #2e7d32; }
.description-text { color: #444; line-height: 1.6; margin: 0; }

.quiz-container { min-height: 80vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
.quiz-card { background: white; width: 100%; max-width: 500px; border-radius: 30px; padding: 40px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center; }
.day-badge { background: #e8f5e9; color: #00a651; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 14px; }
.question-text { font-size: 24px; font-weight: 700; margin: 40px 0; line-height: 1.4; color: #333; }

.answer-btns { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.answer-btns button { height: 100px; font-size: 40px; font-weight: 900; border: none; border-radius: 20px; cursor: pointer; transition: 0.3s; color: white; }
.btn-o { background: #4caf50; }
.btn-x { background: #f44336; }
.answer-btns button:hover { transform: scale(1.05); }

.status-badge { display: inline-block; background: #eee; color: #666; padding: 4px 12px; border-radius: 6px; font-size: 14px; margin-bottom: 10px; }
.answer-info { font-size: 18px; margin-bottom: 15px; }
.answer-info strong { color: #00a651; font-size: 22px; }

.result-section.correct .result-icon { color: #4caf50; font-size: 40px; font-weight: 900; }
.result-section.wrong .result-icon { color: #f44336; font-size: 40px; font-weight: 900; }
.result-section.correct h4 { color: #4caf50; }
.result-section.wrong h4 { color: #f44336; }
.description { background: #f9f9f9; padding: 20px; border-radius: 15px; color: #666; line-height: 1.6; margin-bottom: 30px; }
.back-home-btn { background: #00a651; color: white; border: none; padding: 12px 30px; border-radius: 10px; cursor: pointer; }

.already-done { animation: slideUp 0.5s ease-out; }

@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>