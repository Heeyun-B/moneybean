<template>
  <main class="main-content">
    <div class="page-header">
      <h2 class="page-title">은행 찾기</h2>
    </div>

    <div id="map" class="map-container">
      <div class="search-box">
        <div class="search-header">
          <h3>Money Bean<br>가까운 은행 찾기</h3>
        </div>

        <div class="dropdown-search">
          <select v-model="selectedSido" @change="handleSidoChange" class="search-select">
            <option value="">시/도 선택</option>
            <option v-for="region in mapData" :key="region.name" :value="region.name">
              {{ region.name }}
            </option>
          </select>

          <select v-model="selectedSigungu" @change="handleSigunguChange" :disabled="!selectedSido" class="search-select">
            <option value="">시/군/구 선택</option>
            <option v-for="city in availableCities" :key="city" :value="city">
              {{ city }}
            </option>
          </select>

          <select v-model="selectedBank" :disabled="!selectedSigungu" class="search-select">
            <option value="">은행 선택</option>
            <option v-for="bank in bankList" :key="bank" :value="bank">
              {{ bank }}
            </option>
          </select>

          <button @click="searchBranches" class="search-btn">검색</button>
        </div>
      </div>

      <div class="map-controls">
        <button @click="zoomIn" class="control-btn">+</button>
        <button @click="zoomOut" class="control-btn">-</button>
        <button @click="toggleMyLocation" :class="['control-btn location', { active: isMyLocationActive }]">📍</button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

// 1. 상태 관리 (기존 let 변수들을 ref로 변경)
const mapData = ref([]);
const bankList = ref([]);
const selectedSido = ref('');
const selectedSigungu = ref('');
const selectedBank = ref('');
const isMyLocationActive = ref(false);

let map = null;
let ps = null;
let markers = [];
let infowindows = [];
let myLocationMarker = null;
let myLocationInfowindow = null;

// 2. 시/군/구 데이터 계산
const availableCities = computed(() => {
  const region = mapData.value.find(item => item.name === selectedSido.value);
  return region ? region.countries : [];
});

// 3. 초기화 로직
onMounted(async () => {
  // 데이터 로드
  try {
    const response = await fetch('/data.json');
    mapData.value = (await response.json()).mapInfo;
    const bankRes = await fetch('/data.json');
    bankList.value = (await bankRes.json()).bankInfo;
  } catch (err) {
    console.error("데이터 로드 실패:", err);
  }

  // 지도 초기화
  initMap();
});

const initMap = () => {
  const kakao = window.kakao;
  if (kakao && kakao.maps) {
    kakao.maps.load(() => {
      const container = document.getElementById('map');
      const options = {
        center: new kakao.maps.LatLng(37.49818, 127.027386),
        level: 5
      };
      map = new kakao.maps.Map(container, options);
      ps = new kakao.maps.services.Places();
    });
  }
};

// 4. 이벤트 핸들러
const handleSidoChange = () => {
  selectedSigungu.value = '';
  selectedBank.value = '';
};

const handleSigunguChange = () => {
  selectedBank.value = '';
};

const zoomIn = () => map.setLevel(map.getLevel() - 1);
const zoomOut = () => map.setLevel(map.getLevel() + 1);

const toggleMyLocation = () => {
  if (myLocationMarker) {
    myLocationMarker.setMap(null);
    myLocationMarker = null;
    if (myLocationInfowindow) myLocationInfowindow.close();
    isMyLocationActive.value = false;
    return;
  }

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      const locPosition = new window.kakao.maps.LatLng(position.coords.latitude, position.coords.longitude);
      map.setCenter(locPosition);
      myLocationMarker = new window.kakao.maps.Marker({ position: locPosition, map: map });
      myLocationInfowindow = new window.kakao.maps.InfoWindow({
        content: '<div style="padding:8px; font-size:13px; color:#00a651; font-weight:600;">📍 현재 위치</div>'
      });
      myLocationInfowindow.open(map, myLocationMarker);
      isMyLocationActive.value = true;
    });
  }
};

const searchBranches = () => {
  if (!selectedSido.value || !selectedSigungu.value || !selectedBank.value) {
    alert('항목을 모두 선택해주세요.');
    return;
  }

  // 기존 마커 제거
  markers.forEach(m => m.setMap(null));
  markers = [];
  infowindows.forEach(iw => iw.close());

  const keyword = `${selectedSido.value} ${selectedSigungu.value} ${selectedBank.value}`;
  
  ps.keywordSearch(keyword, (data, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      const bounds = new window.kakao.maps.LatLngBounds();
      data.forEach(place => {
        const marker = new window.kakao.maps.Marker({
          position: new window.kakao.maps.LatLng(place.y, place.x),
          map: map
        });
        markers.push(marker);
        bounds.extend(new window.kakao.maps.LatLng(place.y, place.x));

        const iw = new window.kakao.maps.InfoWindow({
          content: `<div style="padding:15px; min-width:200px;">
                      <h4 style="margin:0 0 5px 0; color:#00a651;">${place.place_name}</h4>
                      <p style="margin:0; font-size:12px; color:#666;">${place.address_name}</p>
                      ${place.phone ? `<p style="margin:5px 0 0 0; font-size:12px; color:#00a651;">📞 ${place.phone}</p>` : ''}
                    </div>`
        });
        infowindows.push(iw);
        window.kakao.maps.event.addListener(marker, 'click', () => {
          infowindows.forEach(i => i.close());
          iw.open(map, marker);
        });
      });
      map.setBounds(bounds);
    } else {
      alert('검색 결과가 없습니다.');
    }
  });
};
</script>

<style scoped>
.main-content { padding: 40px 20px; max-width: 1200px; margin: 0 auto; font-family: 'Pretendard', sans-serif; }
.page-title { font-size: 24px; font-weight: 700; color: #1a1a1a; margin-bottom: 20px; }
.map-container { width: 100%; height: 600px; position: relative; border-radius: 20px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
.search-box { position: absolute; top: 20px; left: 20px; z-index: 10; background: white; padding: 25px; border-radius: 15px; width: 280px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
.search-header h3 { color: #00a651; font-size: 18px; margin-bottom: 20px; }
.search-select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px; }
.search-btn { width: 100%; background: #00a651; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 600; cursor: pointer; }
.map-controls { position: absolute; right: 20px; top: 20px; z-index: 10; display: flex; flex-direction: column; gap: 10px; }
.control-btn { width: 40px; height: 40px; background: white; border: none; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 18px; }
.control-btn.active { background: #00a651; color: white; }
</style>