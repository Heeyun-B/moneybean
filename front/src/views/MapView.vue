<template>
  <main class="main-content">
    <div class="page-header">
      <h2 class="page-title">가까운 은행 찾기</h2>
    </div>

    <div class="bank-finder-wrapper">
      <aside class="search-sidebar">
        <div class="search-header">
          <p class="search-subtitle">지역과 은행을 선택하여 지점을 찾아보세요.</p>
        </div>

        <div class="dropdown-search">
          <div class="select-group">
            <label>시/도</label>
            <select v-model="selectedSido" @change="handleSidoChange" class="search-select">
              <option value="">선택하세요</option>
              <option v-for="region in mapData" :key="region.name" :value="region.name">
                {{ region.name }}
              </option>
            </select>
          </div>

          <div class="select-group">
            <label>시/군/구</label>
            <select v-model="selectedSigungu" @change="handleSigunguChange" :disabled="!selectedSido" class="search-select">
              <option value="">선택하세요</option>
              <option v-for="city in availableCities" :key="city" :value="city">
                {{ city }}
              </option>
            </select>
          </div>

          <div class="select-group">
            <label>은행</label>
            <select v-model="selectedBank" :disabled="!selectedSigungu" class="search-select">
              <option value="">선택하세요</option>
              <option v-for="bank in bankList" :key="bank" :value="bank">
                {{ bank }}
              </option>
            </select>
          </div>

          <button @click="searchBranches" class="search-btn">지점 검색하기</button>
        </div>
      </aside>

      <section class="map-section">
        <div id="map" class="map-container">
          <div class="map-controls">
            <button @click="zoomIn" class="control-btn" title="확대">+</button>
            <button @click="zoomOut" class="control-btn" title="축소">-</button>
            <button @click="toggleMyLocation" :class="['control-btn location', { active: isMyLocationActive }]" title="내 위치">📍</button>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

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

const availableCities = computed(() => {
  const region = mapData.value.find(item => item.name === selectedSido.value);
  return region ? region.countries : [];
});

onMounted(async () => {
  try {
    const response = await fetch('/data.json');
    const data = await response.json();
    mapData.value = data.mapInfo;
    bankList.value = data.bankInfo;
  } catch (err) {
    console.error("데이터 로드 실패:", err);
  }
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
      
      map.setZoomable(true); 
      
      ps = new kakao.maps.services.Places();
    });
  }
};

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
          if (myLocationInfowindow) myLocationInfowindow.close();
          iw.open(map, marker);
        });
      });
      window.kakao.maps.event.addListener(map, 'click', () => {
        infowindows.forEach(i => i.close());
        if (myLocationInfowindow) myLocationInfowindow.close();
      });
      map.setBounds(bounds);
    } else {
      alert('검색 결과가 없습니다.');
    }
  });
};
</script>

<style scoped>
.main-content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Pretendard', sans-serif;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 20px;
  color: #00a651;
}

.bank-finder-wrapper {
  display: flex;
  gap: 20px;
  position: relative;
  height: 600px; 
}

.search-sidebar {
  width: 300px;
  min-width: 300px;
  background: white;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  border: 1px solid #eee;
  z-index: 5;
  display: flex;
  flex-direction: column;
}

.search-header h3 {
  color: #00a651;
  font-size: 18px;
  margin-bottom: 10px;
}

.search-subtitle {
  font-size: 13px;
  color: #666;
  margin-bottom: 20px;
}

.select-group {
  margin-bottom: 15px;
}

.select-group label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
}

.search-select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}

.search-btn {
  width: 100%;
  background: #00a651;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  margin-top: auto;
}

/* 지도 영역 */
.map-section {
  flex: 1;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #eee;
  position: relative;
}

.map-container {
  width: 100%;
  height: 100%;
}

.map-controls {
  position: absolute;
  top: 15px;
  right: 15px;
  z-index: 10;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.control-btn {
  width: 35px;
  height: 35px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.control-btn.active {
  background: #00a651;
  color: white;
  border-color: #00a651;
}

@media (max-width: 850px) {
  .bank-finder-wrapper {
    flex-direction: column;
    height: auto;
  }
  .search-sidebar {
    width: 100%;
    min-width: 100%;
  }
  .map-section {
    height: 400px;
  }
}
</style>