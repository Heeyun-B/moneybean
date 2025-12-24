<template>
  <div class="profile-container" v-if="profileData">
    <div class="profile-main-card">
      <div class="card-bg"></div>
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
              <div class="inline-level-tag" :class="currentLevel.class">
                <img :src="getLevelImg(currentLevel.img)" class="inline-level-img" />
                <span class="inline-level-name">{{ currentLevel.name }}</span>
              </div>
            </div>
            <p class="user-id">@{{ profileData.username }} <span class="divider">|</span> {{ profileData.email }}</p>
            <p v-if="profileData.birth_date" class="user-birth">🎂 {{ profileData.birth_date }}</p>
            <button class="btn-toggle" @click="startEdit">프로필 수정하기</button>
          </template>

          <template v-else>
            <div class="edit-inputs">
              <div class="input-group">
                <label class="input-label">닉네임</label>
                <input type="text" v-model="editNickname" class="input-field" />
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
          </template>
        </div>
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
          <div class="column-header"><span>좋아요한 글</span><span class="count-tag">{{ likedPosts.length }}</span></div>
          <div v-if="likedPosts.length > 0" class="post-mini-list">
            <div v-for="post in likedPosts" :key="post.id" class="post-mini-item" @click="goToPost(post.id)">
              <div class="post-info">
                <span class="post-title">{{ post.title }}</span>
                <span class="post-author">by {{ post.username || '익명' }}</span>
              </div>
              <span class="post-meta">❤️ {{ post.like_count }}</span>
            </div>
          </div>
          <div v-else class="empty-box">좋아요한 게시글이 없습니다.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAssetStore } from '@/stores/asset'
import axios from 'axios'
import defaultLogo from '@/assets/logo_bean.png'

const router = useRouter()
const authStore = useAuthStore()
const assetStore = useAssetStore()

const profileData = ref(null)
const likedPosts = ref([])
const isEditing = ref(false)
const isLoading = ref(false)
const cacheBuster = ref(Date.now())

// 생년월일 수정을 위한 상태
const editNickname = ref('')
const birthYear = ref('1995')
const birthMonth = ref('01')
const birthDay = ref('01')
const selectedFile = ref(null)
const previewUrl = ref(null)

const years = Array.from({ length: 100 }, (_, i) => String(2025 - i))
const months = Array.from({ length: 12 }, (_, i) => String(i + 1).padStart(2, '0'))
const days = computed(() => {
  const lastDay = new Date(parseInt(birthYear.value), parseInt(birthMonth.value), 0).getDate()
  return Array.from({ length: lastDay }, (_, i) => String(i + 1).padStart(2, '0'))
})

const currentLevel = ref({ name: "콩", img: "level_bean.png", class: "lv-1" })

// 이미지 경로 및 캐시 관리
const displayImageUrl = computed(() => {
  if (previewUrl.value) return previewUrl.value
  return authStore.profileImage ? `${authStore.profileImage}?t=${cacheBuster.value}` : defaultLogo
})

const getLevelImg = (imgName) => new URL(`../assets/level_logos/${imgName}`, import.meta.url).href

// 레벨 계산 로직 강화 (total_balance 우선, 없으면 netWorth)
const calculateLevel = () => {
  const balance = profileData.value?.total_balance || assetStore.netWorth || 0
  if (balance >= 100000000) currentLevel.value = { name: "돈나무", img: "level_money_tree.png", class: "lv-5" }
  else if (balance >= 80000000) currentLevel.value = { name: "나무", img: "level_tree.png", class: "lv-4" }
  else if (balance >= 50000000) currentLevel.value = { name: "가지", img: "level_branch.png", class: "lv-3" }
  else if (balance >= 10000000) currentLevel.value = { name: "새싹", img: "level_sprout.png", class: "lv-2" }
  else currentLevel.value = { name: "콩", img: "level_bean.png", class: "lv-1" }
}

const getProfile = async () => {
  try {
    const res = await axios.get(`${authStore.API_URL}/api/accounts/profile/`, {
      headers: { Authorization: `Token ${authStore.token}` }
    })
    profileData.value = res.data
    
    // 좋아요 목록 가져오기
    const likedRes = await axios.get(`${authStore.API_URL}/api/v1/board/liked/`, {
      headers: { Authorization: `Token ${authStore.token}` }
    })
    likedPosts.value = Array.isArray(likedRes.data) ? likedRes.data : []
    
    calculateLevel()
  } catch (err) {
    console.error('데이터 로드 실패:', err)
  }
}

onMounted(async () => {
  await assetStore.getAssets()
  await getProfile()
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
    // 스토어 정보 갱신 및 캐시 무효화
    authStore.updateUserInfo(res.data)
    cacheBuster.value = Date.now()
    await getProfile()
    isEditing.value = false
    previewUrl.value = null
    alert('프로필이 수정되었습니다!')
  } catch (err) {
    alert('수정 실패')
  } finally {
    isLoading.value = false
  }
}

const startEdit = () => {
  editNickname.value = profileData.value.nickname
  if (profileData.value.birth_date) {
    const parts = profileData.value.birth_date.split('-')
    birthYear.value = parts[0]; birthMonth.value = parts[1]; birthDay.value = parts[2]
  }
  isEditing.value = true
}

const cancelEdit = () => { isEditing.value = false; previewUrl.value = null }
const formatDate = (d) => d ? d.split('T')[0] : ''
const goToPost = (id) => router.push({ name: 'board-detail', params: { type: 'free', id: id.toString() } })
const goToProductDetail = (type, id) => router.push({ name: type === 'deposit' ? 'deposit-detail' : 'saving-detail', params: { id } })
</script>

<style scoped>
.profile-container { max-width: 950px; margin: 40px auto; padding: 0 20px; font-family: 'Pretendard', sans-serif; }
.profile-main-card { background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 30px; border: 1px solid #f0f0f0; }
.card-bg { height: 110px; background: linear-gradient(135deg, #00a651 0%, #7ed957 100%); }
.user-content { padding: 0 40px 35px; display: flex; align-items: flex-end; gap: 30px; margin-top: -55px; }

.avatar-box { position: relative; width: 140px; height: 140px; }
.user-avatar { width: 100%; height: 100%; border-radius: 50%; border: 6px solid white; object-fit: cover; background: #f8f8f8; }
.editing-img { filter: brightness(0.5); }
.camera-overlay { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; cursor: pointer; }
.camera-circle { font-size: 30px; color: white; }

.name-area { display: flex; align-items: center; gap: 15px; margin-bottom: 8px; }
.user-nickname { font-size: 28px; font-weight: 800; color: #1a1a1a; margin: 0; }
.inline-level-tag { display: flex; align-items: center; gap: 6px; padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 13px; }
.inline-level-img { width: 20px; height: 20px; }

/* 레벨 테마 */
.lv-1 { background: #f3f4f6; color: #6b7280; }
.lv-2 { background: #ecfdf5; color: #059669; }
.lv-3 { background: #eff6ff; color: #2563eb; }
.lv-4 { background: #faf5ff; color: #9333ea; }
.lv-5 { background: #fffbeb; color: #d97706; }

.user-id { color: #888; margin-bottom: 15px; }
.btn-toggle { background: white; border: 1px solid #00a651; color: #00a651; padding: 8px 20px; border-radius: 10px; font-weight: 700; cursor: pointer; transition: 0.2s; }
.btn-toggle:hover { background: #00a651; color: white; }

/* 수정한 셀렉트 박스 디자인 */
.picker-group { display: flex; gap: 8px; }
.picker-select { padding: 10px; border: 1px solid #ddd; border-radius: 8px; flex: 1; font-weight: 600; cursor: pointer; outline: none; }
.picker-select:focus { border-color: #00a651; }

.asset-grid, .community-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.asset-column, .community-column { background: white; padding: 25px; border-radius: 18px; border: 1px solid #eee; box-shadow: 0 4px 15px rgba(0,0,0,0.02); }
.column-header { display: flex; justify-content: space-between; font-weight: 800; border-bottom: 2px solid #f8f9fa; padding-bottom: 15px; margin-bottom: 15px; }
.count-tag { color: #00a651; font-size: 13px; }

.product-item, .post-mini-item { padding: 15px; border-radius: 12px; border: 1px solid #f5f5f5; margin-bottom: 10px; cursor: pointer; transition: 0.2s; }
.product-item:hover, .post-mini-item:hover { border-color: #00a651; background: #f1fcf4; transform: translateY(-2px); }
.bank { font-size: 11px; color: #00a651; font-weight: 700; }
.title { font-size: 15px; font-weight: 700; margin-top: 4px; }
.info { font-size: 13px; color: #777; margin-top: 5px; }

.post-title { font-weight: 700; font-size: 14px; display: block; }
.post-date, .post-author { font-size: 12px; color: #999; }
.empty-box { text-align: center; padding: 40px; color: #ccc; border: 1px dashed #eee; border-radius: 15px; }

.btn-save { background: #00a651; color: white; border: none; padding: 12px; border-radius: 10px; font-weight: 700; cursor: pointer; flex: 1; }
.btn-cancel { background: #f3f4f6; color: #666; border: none; padding: 12px 20px; border-radius: 10px; cursor: pointer; }
</style>