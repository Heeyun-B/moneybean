<template>
  <div class="profile-container" v-if="profileData">
    <div class="profile-main-card">
      <div class="card-bg">
        <div class="card-level-display">
          <div class="inline-level-tag-top" :class="levelData.class">
            <img :src="levelData.imgUrl" class="inline-level-img-top" />
            <span class="inline-level-name-top">{{ levelData.name }}</span>
          </div>
        </div>
      </div>
      <div class="user-content">
        <div class="avatar-box">
          <img 
            :src="displayImageUrl" 
            :key="cacheBuster"
            class="user-avatar" 
            :class="{ 'editing-img': isEditing }"
          />
          <label v-if="isEditing" for="file-input" class="camera-overlay">
            <div class="camera-circle"><span>📷</span></div>
          </label>
          <input id="file-input" type="file" @change="onFileChange" hidden accept="image/*" />
        </div>

        <div class="user-details">
          <template v-if="!isEditing">
            <div class="name-area">
              <h2 class="user-nickname">{{ profileData.nickname }}님</h2>
            </div>
            <div class="user-info-section">
              <p class="user-id">@{{ profileData.username }} <span class="divider">|</span> {{ profileData.email }}</p>
              <p v-if="profileData.birth_date" class="user-birth">🎂 {{ profileData.birth_date }}</p>
              <button class="btn-toggle" @click="startEdit">프로필 수정하기</button>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- 프로필 수정 폼 -->
    <div v-if="isEditing" class="edit-form-card">
      <div class="edit-form-header">
        <h3>프로필 수정</h3>
      </div>
      <div class="edit-inputs">
        <div class="input-group">
          <label class="input-label">닉네임</label>
          <input type="text" v-model="editNickname" class="input-field" placeholder="닉네임을 입력하세요" />
        </div>
        
        <div class="input-group">
          <label class="input-label">이메일 (선택)</label>
          <input type="email" v-model="editEmail" class="input-field" placeholder="example@email.com" />
        </div>
        
        <div class="input-group">
          <label class="input-label">생년월일</label>
          <div class="picker-group">
            <select v-model="birthYear" class="picker-select">
              <option v-for="y in years" :key="y" :value="y">{{ y }}년</option>
            </select>
            <select v-model="birthMonth" class="picker-select">
              <option v-for="m in months" :key="m" :value="m">{{ m }}월</option>
            </select>
            <select v-model="birthDay" class="picker-select">
              <option v-for="d in days" :key="d" :value="d">{{ d }}일</option>
            </select>
          </div>
        </div>
      </div>
      <div class="edit-actions-row">
        <button class="btn-cancel" @click="cancelEdit">취소</button>
        <button class="btn-save" @click="handleUpdate" :disabled="isLoading">
          {{ isLoading ? '저장 중...' : '변경 완료' }}
        </button>
      </div>
    </div>

    <div class="asset-section" v-if="!isEditing">
      <div class="section-title"><h3>🏦 나의 가입 상품</h3></div>
      <div class="asset-grid">
        <div class="asset-column">
          <div class="column-header">
            <span>💰 정기예금</span>
            <span class="count-tag">{{ profileData.deposit_subscriptions?.length || 0 }}</span>
          </div>
          <div v-if="profileData.deposit_subscriptions?.length > 0" class="product-list">
            <div v-for="item in profileData.deposit_subscriptions" :key="item.id" class="product-item clickable" @click="goToProductDetail('deposit', item.product_code)">
              <div class="bank">{{ item.bank_name }}</div>
              <div class="title">{{ item.product_name }}</div>
              <div class="info">{{ item.interest_rate }}% | {{ item.save_term }}개월</div>
            </div>
          </div>
          <div v-else class="empty-box">가입된 예금이 없습니다.</div>
        </div>

        <div class="asset-column">
          <div class="column-header">
            <span>🐷 정기적금</span>
            <span class="count-tag">{{ profileData.saving_subscriptions?.length || 0 }}</span>
          </div>
          <div v-if="profileData.saving_subscriptions?.length > 0" class="product-list">
            <div v-for="item in profileData.saving_subscriptions" :key="item.id" class="product-item clickable" @click="goToProductDetail('saving', item.product_code)">
              <div class="bank">{{ item.bank_name }}</div>
              <div class="title">{{ item.product_name }}</div>
              <div class="info">{{ item.interest_rate }}% | {{ item.save_term }}개월</div>
            </div>
          </div>
          <div v-else class="empty-box">가입된 적금이 없습니다.</div>
        </div>
      </div>
    </div>

    <div class="community-section" v-if="!isEditing">
      <div class="section-title"><h3>📝 커뮤니티 활동</h3></div>
      <div class="community-grid">
        <div class="community-column">
          <div class="column-header"><span>내 게시글</span><span class="count-tag">{{ profileData.my_posts?.length || 0 }}</span></div>
          <div v-if="profileData.my_posts?.length > 0" class="post-mini-list">
            <div v-for="post in profileData.my_posts" :key="post.id" class="post-mini-item" @click="goToPost(post.id)">
              <div class="post-info"><span class="post-title">{{ post.title }}</span><span class="post-date">{{ formatDate(post.created_at) }}</span></div>
            </div>
          </div>
          <div v-else class="empty-box">작성한 게시글이 없습니다.</div>
        </div>

        <div class="community-column">
          <div class="column-header"><span>좋아요한 글</span><span class="count-tag">{{ likedPostsDisplay.length }}</span></div>
          <div v-if="likedPostsDisplay.length > 0" class="post-mini-list">
            <div v-for="post in likedPostsDisplay" :key="post.id" class="post-mini-item" @click="goToPostWithType(post)">
              <div class="post-info">
                <span class="post-title">{{ post.title }}</span>
                <span class="post-author">by {{ post.author || '익명' }}</span>
              </div>
              <span class="post-meta">❤️ {{ post.like_count || 0 }}</span>
            </div>
          </div>
          <div v-else class="empty-box">좋아요한 게시글이 없습니다.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAssetStore } from '@/stores/asset'
import { useBoardStore } from '@/stores/board'
import axios from 'axios'
import defaultLogo from '@/assets/logo_bean.png'

// 레벨 이미지 import
import levelBeanImg from '@/assets/level_logos/level_bean.png'
import levelSproutImg from '@/assets/level_logos/level_sprout.png'
import levelBranchImg from '@/assets/level_logos/level_branch.png'
import levelTreeImg from '@/assets/level_logos/level_tree.png'
import levelMoneyTreeImg from '@/assets/level_logos/level_money_tree.png'

const router = useRouter()
const authStore = useAuthStore()
const assetStore = useAssetStore()
const boardStore = useBoardStore()

const profileData = ref(null)
const isEditing = ref(false)
const isLoading = ref(false)
const cacheBuster = ref(Date.now())

// 레벨 데이터를 단순 ref로 관리
const levelData = ref({ 
  name: "콩", 
  imgUrl: levelBeanImg, 
  class: "lv-1" 
})

// 생년월일 수정을 위한 상태
const editNickname = ref('')
const editEmail = ref('')
const birthYear = ref('1995')
const birthMonth = ref('01')
const birthDay = ref('01')
const selectedFile = ref(null)
const previewUrl = ref(null)

const years = Array.from({ length: 50 }, (_, i) => String(2025 - i))
const months = Array.from({ length: 12 }, (_, i) => String(i + 1).padStart(2, '0'))
const days = computed(() => {
  const lastDay = new Date(parseInt(birthYear.value), parseInt(birthMonth.value), 0).getDate()
  return Array.from({ length: lastDay }, (_, i) => String(i + 1).padStart(2, '0'))
})

// 좋아요한 게시글 목록
const likedPostsDisplay = computed(() => {
  return boardStore.getLikedPosts().slice(0, 5)
})

// 이미지 경로
const displayImageUrl = computed(() => {
  if (previewUrl.value) return previewUrl.value
  return authStore.profileImage ? `${authStore.profileImage}?t=${cacheBuster.value}` : defaultLogo
})

// 레벨 계산 함수
const calculateLevel = () => {
  // assetStore에서 직접 값 가져오기
  const balance = assetStore.netWorth || profileData.value?.total_balance || 0
  
  console.log('🎯 레벨 계산:', balance.toLocaleString())
  
  if (balance >= 100000000) {
    levelData.value = { name: "돈나무", imgUrl: levelMoneyTreeImg, class: "lv-5" }
  } else if (balance >= 80000000) {
    levelData.value = { name: "나무", imgUrl: levelTreeImg, class: "lv-4" }
  } else if (balance >= 50000000) {
    levelData.value = { name: "가지", imgUrl: levelBranchImg, class: "lv-3" }
  } else if (balance >= 10000000) {
    levelData.value = { name: "새싹", imgUrl: levelSproutImg, class: "lv-2" }
  } else {
    levelData.value = { name: "콩", imgUrl: levelBeanImg, class: "lv-1" }
  }
  
  console.log('✅ 레벨:', levelData.value.name)
}

const getProfile = async () => {
  try {
    const res = await axios.get(`${authStore.API_URL}/api/accounts/profile/`, {
      headers: { Authorization: `Token ${authStore.token}` }
    })
    profileData.value = res.data
    console.log('📋 프로필 로드 완료')
    
    // 프로필 로드 후 레벨 계산
    calculateLevel()
  } catch (err) {
    console.error('❌ 프로필 로드 실패:', err)
  }
}

onMounted(async () => {
  console.log('🚀 ProfileView 마운트')
  
  try {
    // 1. 자산 데이터 로드
    console.log('💰 자산 로드 시작...')
    await assetStore.getAssets()
    await assetStore.getCategories()
    
    console.log('자산 데이터:', {
      netWorth: assetStore.netWorth,
      totalAssets: assetStore.totalAssets,
      totalDebt: assetStore.totalDebt
    })
    
    // 자산 로드 직후 레벨 계산
    calculateLevel()
    
    // 2. 게시판 데이터 로드 (백그라운드)
    Promise.all([
      boardStore.fetchPosts('free'),
      boardStore.fetchPosts('news'),
      boardStore.fetchPosts('info')
    ])
    
    // 3. 프로필 로드
    await getProfile()
    
    // 최종 한번 더 계산
    calculateLevel()
    
    console.log('✅ 초기화 완료')
  } catch (error) {
    console.error('❌ 초기화 오류:', error)
  }
})

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    selectedFile.value = file
    previewUrl.value = URL.createObjectURL(file)
  }
}

const handleUpdate = async () => {
  isLoading.value = true
  const formData = new FormData()
  formData.append('nickname', editNickname.value)
  
  if (editEmail.value && editEmail.value.trim() !== '') {
    formData.append('email', editEmail.value.trim())
  }
  
  const fullDate = `${birthYear.value}-${birthMonth.value}-${birthDay.value}`
  formData.append('birth_date', fullDate)
  if (selectedFile.value) formData.append('profile_image', selectedFile.value)

  try {
    const res = await axios.put(`${authStore.API_URL}/api/accounts/profile/update/`, formData, {
      headers: { 
        'Authorization': `Token ${authStore.token}`,
        'Content-Type': 'multipart/form-data' 
      }
    })
    authStore.updateUserInfo(res.data)
    cacheBuster.value = Date.now()
    await getProfile()
    isEditing.value = false
    previewUrl.value = null
    selectedFile.value = null
    alert('프로필이 수정되었습니다!')
  } catch (err) {
    console.error('프로필 수정 실패:', err)
    alert('수정 실패: ' + (err.response?.data?.error || '알 수 없는 오류'))
  } finally {
    isLoading.value = false
  }
}

const startEdit = () => {
  editNickname.value = profileData.value.nickname
  editEmail.value = profileData.value.email || ''
  if (profileData.value.birth_date) {
    const parts = profileData.value.birth_date.split('-')
    birthYear.value = parts[0]
    birthMonth.value = parts[1]
    birthDay.value = parts[2]
  }
  isEditing.value = true
}

const cancelEdit = () => { 
  isEditing.value = false
  previewUrl.value = null
  selectedFile.value = null
}

const formatDate = (d) => d ? d.split('T')[0] : ''

const goToPost = (id) => {
  router.push({ 
    name: 'board-detail', 
    params: { type: 'free', id: id.toString() } 
  })
}

const goToPostWithType = (post) => {
  const boardType = post.boardType || 'free'
  router.push({ 
    name: 'board-detail', 
    params: { type: boardType, id: post.id.toString() } 
  })
}

const goToProductDetail = (type, id) => {
  router.push({ 
    name: type === 'deposit' ? 'deposit-detail' : 'saving-detail', 
    params: { id } 
  })
}
</script>

<style scoped>
.profile-container { max-width: 950px; margin: 40px auto; padding: 0 20px; font-family: 'Pretendard', sans-serif; }

/* 메인 프로필 카드 */
.profile-main-card { 
  background: white; 
  border-radius: 20px; 
  overflow: hidden; 
  box-shadow: 0 10px 30px rgba(0,0,0,0.05); 
  margin-bottom: 30px; 
  border: 1px solid #f0f0f0; 
}

.card-bg { 
  height: 110px; 
  background: linear-gradient(135deg, #00a651 0%, #7ed957 100%); 
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 40px;
}

.card-level-display {
  position: absolute;
  top: 20px;
  right: 30px;
}

.inline-level-tag-top { 
  display: flex; 
  align-items: center; 
  gap: 8px; 
  padding: 8px 18px; 
  border-radius: 25px; 
  font-weight: 700; 
  font-size: 14px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.inline-level-img-top { 
  width: 24px; 
  height: 24px; 
  object-fit: contain; 
}

.inline-level-name-top {
  font-weight: 800;
}

/* 레벨 테마 */
.inline-level-tag-top.lv-1 { color: #6b7280; }
.inline-level-tag-top.lv-2 { color: #059669; }
.inline-level-tag-top.lv-3 { color: #2563eb; }
.inline-level-tag-top.lv-4 { color: #9333ea; }
.inline-level-tag-top.lv-5 { color: #d97706; }

.user-content { 
  padding: 0 40px 35px; 
  display: flex; 
  align-items: flex-start; 
  gap: 30px; 
  margin-top: -55px; 
}

.avatar-box { 
  position: relative; 
  width: 140px; 
  height: 140px; 
  flex-shrink: 0; 
}

.user-avatar { 
  width: 100%; 
  height: 100%; 
  border-radius: 50%; 
  border: 6px solid white; 
  object-fit: cover; 
  background: #f8f8f8; 
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.editing-img { filter: brightness(0.5); }
.camera-overlay { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; cursor: pointer; }
.camera-circle { font-size: 30px; color: white; }

.user-details { 
  flex: 1; 
  padding-top: 60px;
}

.name-area { 
  margin-bottom: 5px; 
}

.user-nickname { 
  font-size: 28px; 
  font-weight: 800; 
  color: #1a1a1a; 
  margin: 0; 
}

/* 사용자 정보 섹션 - 간격 추가 */
.user-info-section {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}

.user-id { 
  color: #888; 
  margin: 0 0 10px 0; 
  font-size: 14px; 
}

.divider { margin: 0 8px; }

.user-birth { 
  color: #666; 
  font-size: 14px; 
  margin: 0 0 15px 0; 
}

.btn-toggle { 
  background: white; 
  border: 1px solid #00a651; 
  color: #00a651; 
  padding: 10px 24px; 
  border-radius: 10px; 
  font-weight: 700; 
  cursor: pointer; 
  transition: 0.2s;
  font-size: 14px;
  display: inline-block;
}

.btn-toggle:hover { 
  background: #00a651; 
  color: white; 
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3);
}

/* 수정 폼 카드 */
.edit-form-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  margin-bottom: 30px;
  border: 1px solid #f0f0f0;
}

.edit-form-header {
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f0f0;
}

.edit-form-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 800;
  color: #1a1a1a;
}

.edit-inputs { margin-bottom: 25px; }
.input-group { margin-bottom: 20px; }
.input-label { 
  display: block; 
  font-weight: 600; 
  margin-bottom: 10px; 
  color: #333; 
  font-size: 14px;
}

.input-field { 
  width: 100%; 
  padding: 12px 15px; 
  border: 1px solid #ddd; 
  border-radius: 10px; 
  font-size: 14px;
  transition: border-color 0.2s;
  font-family: 'Pretendard', sans-serif;
}

.input-field:focus { 
  outline: none; 
  border-color: #00a651; 
  box-shadow: 0 0 0 3px rgba(0, 166, 81, 0.1);
}

.picker-group { display: flex; gap: 10px; }
.picker-select { 
  padding: 12px 15px; 
  border: 1px solid #ddd; 
  border-radius: 10px; 
  flex: 1; 
  font-weight: 600; 
  cursor: pointer; 
  outline: none;
  font-family: 'Pretendard', sans-serif;
  transition: border-color 0.2s;
}

.picker-select:focus { 
  border-color: #00a651; 
  box-shadow: 0 0 0 3px rgba(0, 166, 81, 0.1);
}

.edit-actions-row { 
  display: flex; 
  gap: 12px; 
  margin-top: 30px;
}

.btn-save { 
  background: #00a651; 
  color: white; 
  border: none; 
  padding: 14px; 
  border-radius: 10px; 
  font-weight: 700; 
  cursor: pointer; 
  flex: 1; 
  transition: 0.2s;
  font-size: 15px;
}

.btn-save:hover { 
  background: #008f43; 
  transform: translateY(-1px); 
  box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3); 
}

.btn-save:disabled { 
  background: #ccc; 
  cursor: not-allowed; 
  transform: none; 
  box-shadow: none; 
}

.btn-cancel { 
  background: #f3f4f6; 
  color: #666; 
  border: none; 
  padding: 14px 24px; 
  border-radius: 10px; 
  cursor: pointer; 
  transition: 0.2s;
  font-weight: 600;
  font-size: 15px;
}

.btn-cancel:hover { 
  background: #e5e7eb; 
  color: #333; 
}

/* 자산/커뮤니티 섹션 */
.asset-section, .community-section { 
  background: white; 
  border-radius: 20px; 
  padding: 30px; 
  box-shadow: 0 10px 30px rgba(0,0,0,0.05); 
  margin-bottom: 30px; 
  border: 1px solid #f0f0f0; 
}

.section-title h3 { 
  font-size: 20px; 
  font-weight: 800; 
  margin: 0 0 20px 0; 
  color: #1a1a1a; 
}

.asset-grid, .community-grid { 
  display: grid; 
  grid-template-columns: 1fr 1fr; 
  gap: 20px; 
}

.asset-column, .community-column { 
  background: #fafafa; 
  padding: 25px; 
  border-radius: 18px; 
  border: 1px solid #eee; 
}

.column-header { 
  display: flex; 
  justify-content: space-between; 
  font-weight: 800; 
  border-bottom: 2px solid #e8e8e8; 
  padding-bottom: 15px; 
  margin-bottom: 15px;
  font-size: 15px;
}

.count-tag { color: #00a651; font-size: 13px; }

.product-list, .post-mini-list { max-height: 300px; overflow-y: auto; }

.product-item, .post-mini-item { 
  padding: 15px; 
  border-radius: 12px; 
  border: 1px solid #f5f5f5; 
  margin-bottom: 10px; 
  cursor: pointer; 
  transition: 0.2s;
  background: white;
}

.product-item:hover, .post-mini-item:hover { 
  border-color: #00a651; 
  background: #f1fcf4; 
  transform: translateY(-2px); 
  box-shadow: 0 4px 12px rgba(0, 166, 81, 0.1);
}

.bank { 
  font-size: 11px; 
  color: #00a651; 
  font-weight: 700; 
  text-transform: uppercase; 
}

.title { 
  font-size: 15px; 
  font-weight: 700; 
  margin-top: 4px; 
  color: #333; 
}

.info { 
  font-size: 13px; 
  color: #777; 
  margin-top: 5px; 
}

.post-info { 
  display: flex; 
  flex-direction: column; 
  gap: 4px; 
}

.post-title { 
  font-weight: 700; 
  font-size: 14px; 
  color: #333; 
}

.post-date, .post-author { 
  font-size: 12px; 
  color: #999; 
}

.post-meta { 
  font-size: 12px; 
  color: #ff6b6b; 
  margin-top: 5px; 
  display: inline-block; 
}

.empty-box { 
  text-align: center; 
  padding: 40px; 
  color: #ccc; 
  border: 1px dashed #e8e8e8; 
  border-radius: 15px;
  background: white;
}

@media (max-width: 768px) {
  .asset-grid, .community-grid { grid-template-columns: 1fr; }
  .user-content { flex-direction: column; align-items: center; text-align: center; }
  .avatar-box { margin-bottom: 20px; }
  .picker-group { flex-direction: column; }
  .card-level-display { position: static; margin-bottom: 10px; }
  .user-details { padding-top: 0; }
  .user-info-section { border-top: none; }
}
</style>