<template>
  <div class="create-container">
    <div class="header-area">
      <h1>내 자산 관리</h1>
      <p class="sub-text">왼쪽에서 자산을 추가/수정하고, 오른쪽에서 전체 목록을 확인하세요.<br>
        <strong>드래그하여 순서를 변경</strong>할 수 있으며, 작업 후 <strong>'모든 변경사항 저장하기'</strong>를 꼭 눌러주세요.
      </p>
    </div>

    <div class="main-layout">
      
      <div class="left-section">
        <div class="input-card">
          <h3 class="card-title">
            {{ isEditing ? '✏️ 자산 정보 수정' : '📝 신규 자산 입력' }}
            <button v-if="isEditing" class="cancel-edit-btn" @click="cancelEdit">입력모드로 전환</button>
          </h3>
          
          <div class="form-group">
            <label>자산 분류</label>
            <div class="major-type-group">
              <button 
                type="button" 
                v-for="type in majorTypes" 
                :key="type.key"
                :class="['type-btn', { active: selectedMajor === type.key }]"
                @click="selectMajorType(type.key)"
              >
                {{ type.label }}
              </button>
            </div>
          </div>

          <div class="form-group">
            <label>상세 종류</label>
            <select v-model="formData.category" class="custom-select">
              <option disabled value="">
                {{ store.categories.length === 0 ? '로딩 중...' : '선택해주세요' }}
              </option>
              <option v-for="cat in filteredSubCategories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>이름</label>
            <input 
              type="text" 
              v-model="formData.name" 
              :placeholder="namePlaceholder" 
              class="custom-input"
              @keyup.enter="reflectToLocalList"
            />
          </div>

          <div class="form-group mb-large">
            <label>금액 (원)</label>
            <input 
              type="text" 
              :value="displayAmount"
              @input="onInputAmount($event, 'current_value')"
              placeholder="0" 
              class="custom-input money-input"
              @keyup.enter="reflectToLocalList"
            />
            <p class="korean-money" v-if="formData.current_value > 0">
              {{ formatKoreanNumber(formData.current_value) }}원
            </p>
          </div>

          <button type="button" :class="['reflect-btn', { edit: isEditing }]" @click="reflectToLocalList">
            {{ isEditing ? '수정사항 반영하기 💾' : '목록에 추가하기 ⬇️' }}
          </button>
        </div>

        <div class="input-card financial-card">
          <h3 class="card-title">💰 월 평균 수입/지출</h3>
          <div class="row-group">
            <div class="form-group half mb-large">
              <label>수입</label>
              <input 
                type="text" 
                :value="displayIncome"
                @input="onInputAmount($event, 'income')"
                placeholder="0" 
                class="custom-input money-input"
              />
              <p class="korean-money small" v-if="financialData.income > 0">
                {{ formatKoreanNumber(financialData.income) }}원
              </p>
            </div>
            <div class="form-group half mb-large">
              <label>지출</label>
              <input 
                type="text" 
                :value="displayExpense"
                @input="onInputAmount($event, 'expense')"
                placeholder="0" 
                class="custom-input money-input"
              />
              <p class="korean-money small" v-if="financialData.expense > 0">
                {{ formatKoreanNumber(financialData.expense) }}원
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="right-section">
        <div class="preview-card">
          <div class="preview-header">
            <h3>📊 자산 현황표</h3>
            <span class="total-badge">총 {{ formatWithComma(currentTotalValue) }}원</span>
          </div>

          <div v-if="isLoading" class="loading-box">데이터를 불러오는 중...</div>

          <div v-else class="financial-statement">
            
            <div v-for="type in majorTypes" :key="type.key" class="asset-section">
              <div class="section-header">
                <h4>{{ type.label }}</h4>
                <span :class="['section-total', type.key]">
                  {{ formatWithComma(getSectionTotal(type.key)) }}원
                </span>
              </div>

              <draggable 
                :model-value="getAssetsByGroup(type.key)"
                @update:model-value="(newList) => updateGroupOrder(type.key, newList)"
                item-key="tempId"
                class="section-list"
                handle=".drag-handle"
                :group="type.key" 
                ghost-class="ghost-item"
                :animation="200"
              >
                <template #item="{ element: asset }">
                  <li :class="['asset-row', { 'is-new': !asset.id, 'is-modified': asset.isModified }]">
                    <div class="row-left">
                      <span class="drag-handle">≡</span>
                      <span class="row-cat">{{ getCategoryName(asset.category) }}</span>
                      <span class="row-name">{{ asset.name }}</span>
                      <span v-if="!asset.id" class="badge-new">NEW</span>
                      <span v-if="asset.isModified" class="badge-mod">수정됨</span>
                    </div>
                    <div class="row-right">
                      <span class="row-value">{{ formatWithComma(asset.current_value) }}원</span>
                      <div class="row-actions">
                        <button class="action-btn edit" @click="startEdit(asset)">✏️</button>
                        <button class="action-btn del" @click="deleteLocalAsset(asset)">🗑️</button>
                      </div>
                    </div>
                  </li>
                </template>
              </draggable>

              <div v-if="getAssetsByGroup(type.key).length === 0" class="empty-row">
                등록된 {{ type.label.split(' ')[1] }}이 없습니다.
              </div>
            </div>

          </div>

          <div class="submit-area">
            <button type="button" class="submit-all-btn" @click="saveAllChanges">
              모든 변경사항 저장하기 (완료)
            </button>
            <p class="submit-info">* 순서 변경 및 수정 내용은 저장 버튼을 눌러야 반영됩니다.</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAssetStore } from '@/stores/asset'
import { useRouter } from 'vue-router'
import draggable from 'vuedraggable' // [추가] 라이브러리 임포트

const store = useAssetStore()
const router = useRouter()

// 1. 설정 및 상태
const majorTypes = [
  { key: 'cash', label: '💵 현금성 자산', placeholder: '예: 비상금 통장' },
  { key: 'invest', label: '📈 투자 자산', placeholder: '예: 삼성전자' },
  { key: 'debt', label: '💸 부채', placeholder: '예: 학자금 대출' }
]
const selectedMajor = ref('cash') 
const isLoading = ref(true)

// 입력 폼 데이터
const formData = ref({ category: '', name: '', current_value: null })
// 재정 정보
const financialData = ref({ income: null, expense: null })

// 로컬 상태 관리
const localAssets = ref([])       
const deletedAssetIds = ref([])   
const editingAssetTempId = ref(null) 

const isEditing = computed(() => editingAssetTempId.value !== null)

// 2. 초기 데이터 로드
onMounted(async () => {
  await store.getCategories()
  await store.getAssets()
  await store.getFinancialInfo()
  
  localAssets.value = store.assets.map(asset => ({
    ...asset,
    tempId: `existing_${asset.id}`, 
    isModified: false
  }))

  financialData.value.income = store.financialInfo.income
  financialData.value.expense = store.financialInfo.expense
  
  isLoading.value = false
})

// 3. 폼 관련 Computed & Methods (기존 유지)
const filteredSubCategories = computed(() => {
  if (!store.categories) return []
  const groupMap = { 'cash': 'CASH', 'invest': 'INVEST', 'debt': 'DEBT' }
  return store.categories.filter(cat => cat.group === groupMap[selectedMajor.value])
})

const namePlaceholder = computed(() => {
  const type = majorTypes.find(t => t.key === selectedMajor.value)
  return type ? type.placeholder : '이름 입력'
})

const selectMajorType = (key) => {
  selectedMajor.value = key
  if (!isEditing.value) formData.value.category = '' 
}

// 4. 목록 반영 (추가/수정) (기존 유지)
const reflectToLocalList = () => {
  if (!formData.value.category) return alert('상세 종류를 선택해주세요.')
  if (!formData.value.name) return alert('자산 이름을 입력해주세요.')
  if (formData.value.current_value === null || formData.value.current_value === '') return alert('금액을 입력해주세요.')

  if (isEditing.value) {
    const index = localAssets.value.findIndex(a => a.tempId === editingAssetTempId.value)
    if (index !== -1) {
      localAssets.value[index] = {
        ...localAssets.value[index],
        category: formData.value.category,
        name: formData.value.name,
        current_value: formData.value.current_value,
        isModified: true 
      }
    }
    cancelEdit() 
  } else {
    localAssets.value.push({
      tempId: `new_${Date.now()}`, 
      id: null, 
      category: formData.value.category,
      name: formData.value.name,
      current_value: formData.value.current_value,
      isModified: false
    })
    formData.value.name = ''
    formData.value.current_value = null
  }
}

// 5. 수정/삭제 로직 (기존 유지)
const startEdit = (asset) => {
  const cat = store.categories.find(c => c.id === asset.category)
  if (cat) {
    const groupMapReverse = { 'CASH': 'cash', 'INVEST': 'invest', 'DEBT': 'debt' }
    selectedMajor.value = groupMapReverse[cat.group] || 'cash'
  }
  formData.value = {
    category: asset.category,
    name: asset.name,
    current_value: asset.current_value
  }
  editingAssetTempId.value = asset.tempId 
}

const cancelEdit = () => {
  editingAssetTempId.value = null
  formData.value = { category: '', name: '', current_value: null }
}

const deleteLocalAsset = (asset) => {
  if (!confirm('목록에서 삭제하시겠습니까? (저장 시 최종 반영됨)')) return
  if (asset.id) {
    deletedAssetIds.value.push(asset.id)
  }
  localAssets.value = localAssets.value.filter(a => a.tempId !== asset.tempId)
  if (editingAssetTempId.value === asset.tempId) cancelEdit()
}

// 6. [NEW] 드래그 앤 드롭 순서 변경 로직
const updateGroupOrder = (groupKey, newOrderedList) => {
  // 1. 현재 변경된 그룹이 아닌, 다른 그룹의 아이템들만 추출
  const otherItems = localAssets.value.filter(asset => {
    // 해당 자산의 그룹 키 확인
    const cat = store.categories.find(c => c.id === asset.category)
    const groupMapReverse = { 'CASH': 'cash', 'INVEST': 'invest', 'DEBT': 'debt' }
    const assetGroupKey = cat ? groupMapReverse[cat.group] : null
    
    // 현재 그룹 키와 다른 것만 남김
    return assetGroupKey !== groupKey
  })

  // 2. (다른 그룹 아이템들) + (순서가 변경된 현재 그룹 아이템들) 합치기
  // 주의: 이렇게 하면 localAssets 내부에서의 절대적인 순서는 바뀌지만,
  // 화면은 그룹별로 필터링해서 보여주므로 사용자 눈에는 해당 그룹 내 순서 변경이 잘 적용된 것으로 보임.
  localAssets.value = [...otherItems, ...newOrderedList]
}

// 7. 저장 로직 (기존 유지)
const saveAllChanges = async () => {
  if (!confirm('현재 순서와 내용으로 저장하시겠습니까?')) return

  try {
    const promises = []

    // 1. 삭제 처리 (기존 동일)
    for (const id of deletedAssetIds.value) {
      promises.push(store.deleteAsset(id))
    }

    // 2. 추가 및 수정 처리 (+ 순서 반영)
    // localAssets는 이미 사용자가 드래그해서 순서를 바꾼 상태입니다.
    localAssets.value.forEach((asset, index) => {
      
      const payload = {
        category: asset.category,
        name: asset.name,
        current_value: asset.current_value,
        
        // 현재 리스트의 인덱스(+1)를 순서(order)로 저장
        order: index + 1 
      }

      if (!asset.id) {
        // 신규 -> POST
        promises.push(store.addAsset(payload))
      } else {
        // 기존 -> PUT (순서가 바뀌었을 수 있으므로 업데이트)
        promises.push(store.updateAsset(asset.id, payload))
      }
    })

    // 3. 재정 정보 저장 (기존 동일)
    promises.push(store.saveFinancialInfo(financialData.value))

    await Promise.all(promises)
    
    // 저장 후 최신 데이터(정렬된 상태) 다시 불러오기
    await store.getAssets() 

    alert('저장 완료!')
    router.push({ name: 'assets' })

  } catch (err) {
    console.error(err)
    alert('오류 발생')
  }
}

// 8. 뷰 헬퍼 함수
const getAssetsByGroup = (groupKey) => {
  const groupMap = { 'cash': 'CASH', 'invest': 'INVEST', 'debt': 'DEBT' }
  const targetGroup = groupMap[groupKey]
  
  // localAssets 순서대로 필터링되므로, localAssets 순서를 바꾸면 여기 결과 순서도 바뀜
  return localAssets.value.filter(asset => {
    const cat = store.categories.find(c => c.id === asset.category)
    return cat && cat.group === targetGroup
  })
}

const getSectionTotal = (groupKey) => {
  return getAssetsByGroup(groupKey).reduce((sum, a) => sum + Number(a.current_value), 0)
}

const currentTotalValue = computed(() => {
  return localAssets.value.reduce((sum, a) => sum + Number(a.current_value), 0)
})

const getCategoryName = (id) => {
  const cat = store.categories.find(c => c.id === id)
  return cat ? cat.name : '-'
}

// 9. 포맷팅 함수들 (기존 유지)
const displayAmount = computed(() => formatWithComma(formData.value.current_value))
const displayIncome = computed(() => formatWithComma(financialData.value.income))
const displayExpense = computed(() => formatWithComma(financialData.value.expense))

const onInputAmount = (event, field) => {
  const rawValue = event.target.value.replace(/[^0-9]/g, '')
  const numberValue = rawValue ? Number(rawValue) : 0
  if (field === 'current_value') formData.value.current_value = numberValue
  if (field === 'income') financialData.value.income = numberValue
  if (field === 'expense') financialData.value.expense = numberValue
  event.target.value = formatWithComma(numberValue)
}

const formatWithComma = (val) => {
  if (!val && val !== 0) return ''
  return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

const formatKoreanNumber = (num) => {
  if (!num) return ''
  const units = ['', '만', '억', '조', '경']
  let result = ''
  let number = num
  let unitIndex = 0
  while (number > 0) {
    const mod = number % 10000
    if (mod > 0) result = `${mod.toLocaleString()}${units[unitIndex]} ` + result
    number = Math.floor(number / 10000)
    unitIndex++
  }
  return result.trim() 
}
</script>

<style scoped>
/* 기존 스타일은 그대로 유지하고, 드래그 관련 스타일만 추가/수정합니다 */
.create-container { max-width: 1100px; margin: 0 auto; padding: 40px 20px; }
.header-area { text-align: center; margin-bottom: 40px; }
.sub-text { color: #666; font-size: 14px; margin-top: 10px; line-height: 1.5; }
.main-layout { display: grid; grid-template-columns: 400px 1fr; gap: 30px; align-items: start; }

.input-card, .preview-card {
  background: white; border-radius: 16px; padding: 25px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; margin-bottom: 20px;
}
.card-title { 
  font-size: 18px; margin-bottom: 20px; color: #333; 
  border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;
  display: flex; justify-content: space-between; align-items: center;
}
.cancel-edit-btn { font-size: 12px; background: #eee; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; }

/* Form Styles */
.form-group { margin-bottom: 20px; display: flex; flex-direction: column; position: relative; }
.form-group.mb-large { margin-bottom: 30px; }
label { font-size: 13px; font-weight: bold; color: #555; margin-bottom: 8px; }
.major-type-group { display: flex; gap: 5px; }
.type-btn { flex: 1; padding: 10px 0; border: 1px solid #ddd; background: #fafafa; border-radius: 8px; cursor: pointer; font-size: 13px; color: #666; transition: 0.2s; }
.type-btn.active { background: #e8f5e9; border-color: #00a651; color: #00a651; font-weight: bold; }
.custom-input, .custom-select { padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 15px; outline: none; transition: 0.2s; width: 100%; box-sizing: border-box; }
.custom-input:focus, .custom-select:focus { border-color: #00a651; }
.money-input { text-align: right; color: #00a651; font-weight: bold; }
.korean-money { position: absolute; bottom: -25px; right: 0; font-size: 12px; color: #00a651; font-weight: bold; background: #e8f5e9; padding: 2px 6px; border-radius: 4px; z-index: 10; }
.reflect-btn { width: 100%; padding: 15px; background: #333; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 5px; transition: 0.2s; }
.reflect-btn:hover { background: #555; }
.reflect-btn.edit { background: #0288d1; }
.reflect-btn.edit:hover { background: #0277bd; }

/* Right Section Styles */
.right-section { position: sticky; top: 100px; }
.preview-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px; border-bottom: 2px solid #333; padding-bottom: 15px; }
.total-badge { font-size: 20px; font-weight: bold; color: #00a651; }
.financial-statement { display: flex; flex-direction: column; gap: 30px; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; background: #f9f9f9; padding: 8px 12px; border-radius: 6px; }
.section-header h4 { margin: 0; font-size: 15px; color: #555; }
.section-total { font-weight: bold; font-size: 15px; }
.section-total.debt { color: #e53935; }

/* Draggable List Styles */
.section-list { 
  list-style: none; padding: 0; min-height: 20px; /* 드래그 영역 확보 */
}

/* [NEW] 드래그 고스트 스타일 (이동 중인 아이템의 잔상) */
.ghost-item {
  opacity: 0.5;
  background: #e8f5e9;
  border: 2px dashed #00a651;
}

.asset-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 5px; border-bottom: 1px solid #eee; background: white; }
.asset-row:hover { background: #fcfcfc; }
.asset-row.is-new { background: #e8f5e9; }
.asset-row.is-modified { background: #e1f5fe; }

/* [NEW] 드래그 핸들 스타일 */
.drag-handle {
  cursor: grab;
  color: #ccc;
  margin-right: 8px;
  font-size: 18px;
  user-select: none;
}
.drag-handle:active { cursor: grabbing; color: #00a651; }

.row-left { display: flex; align-items: center; gap: 8px; }
.row-cat { font-size: 12px; color: #666; background: #eee; padding: 2px 6px; border-radius: 4px; }
.row-name { font-size: 15px; font-weight: 500; color: #333; }
.badge-new { font-size: 10px; background: #00a651; color: white; padding: 2px 4px; border-radius: 4px; }
.badge-mod { font-size: 10px; background: #0288d1; color: white; padding: 2px 4px; border-radius: 4px; }

.row-right { display: flex; align-items: center; gap: 15px; }
.row-value { font-weight: bold; font-size: 15px; color: #333; }
.row-actions { display: flex; gap: 5px; }
.action-btn { background: none; border: 1px solid #eee; border-radius: 4px; cursor: pointer; padding: 4px; font-size: 14px; transition: 0.2s; }
.action-btn:hover { background: #f0f0f0; }
.action-btn.del:hover { background: #ffebee; border-color: #ffcdd2; }

.empty-row { text-align: center; color: #ccc; padding: 10px; font-size: 13px; }

.submit-area { margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; text-align: center; }
.submit-all-btn { width: 100%; padding: 18px; background: #00a651; color: white; border: none; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer; box-shadow: 0 5px 15px rgba(0, 166, 81, 0.3); transition: 0.2s; }
.submit-all-btn:hover { background: #008e45; transform: translateY(-2px); }
.submit-info { font-size: 12px; color: #888; margin-top: 10px; }
.loading-box { text-align: center; padding: 50px; color: #999; }

@media (max-width: 900px) {
  .main-layout { grid-template-columns: 1fr; }
  .right-section { position: static; }
}
</style>