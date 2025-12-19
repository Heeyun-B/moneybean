// 전역 변수
let map; // 카카오맵 객체
let markers = []; // 마커 배열
let infowindows = []; // 인포윈도우 배열
let ps; // 장소 검색 객체
let regionData = null; // JSON 데이터 저장
let myLocationMarker = null; // 내 위치 마커
let myLocationInfowindow = null; // 내 위치 인포윈도우

// data.json 파일 로드
async function loadDataJSON() {
    try {
        const response = await fetch('data.json');
        if (!response.ok) {
            throw new Error('data.json 파일을 불러올 수 없습니다.');
        }
        regionData = await response.json();
        console.log('데이터 로드 완료:', regionData);
        return true;
    } catch (error) {
        console.error('데이터 로드 실패:', error);
        alert('지역 데이터를 불러오는데 실패했습니다.');
        return false;
    }
}

// 카카오맵 SDK 동적 로드
function loadKakaoMapSDK() {
    // API_KEY 변수 사용 및 autoload=false 옵션 추가
    const scriptSrc = "//dapi.kakao.com/v2/maps/sdk.js?appkey=" + API_KEY + "&autoload=false&libraries=services";
    
    // SDK 스크립트 태그를 동적으로 생성하여 문서에 삽입
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = scriptSrc;
    document.head.appendChild(script);

    // kakao.maps.load()를 사용하여 SDK 로드가 완료된 후 지도를 생성
    script.onload = function() {
        kakao.maps.load(function() {
            initMap();
            initDropdowns();
            loadSidoOptions();
        });
    };
}

// 지도 초기화
function initMap() {
    const container = document.getElementById('map'); // 지도를 담을 영역의 DOM 레퍼런스
    const options = {
        center: new kakao.maps.LatLng(37.49818, 127.027386), // 초기 좌표
        level: 5 // 지도의 레벨(확대, 축소 정도)
    };

    map = new kakao.maps.Map(container, options); // 지도 생성 및 객체 리턴
    ps = new kakao.maps.services.Places(); // 장소 검색 객체 생성

    // 지도 컨트롤 설정
    setupMapControls();
}

// 지도 컨트롤 설정
function setupMapControls() {
    // 줌 인 버튼
    document.querySelector('.zoom-in').addEventListener('click', function() {
        const level = map.getLevel();
        map.setLevel(level - 1);
    });

    // 줌 아웃 버튼
    document.querySelector('.zoom-out').addEventListener('click', function() {
        const level = map.getLevel();
        map.setLevel(level + 1);
    });

    // 내 위치 버튼
    const locationBtn = document.querySelector('.location');
    
    locationBtn.addEventListener('click', function() {
        // 이미 내 위치 마커가 있으면 제거 (토글 기능)
        if (myLocationMarker) {
            myLocationMarker.setMap(null);
            myLocationMarker = null;
            
            if (myLocationInfowindow) {
                myLocationInfowindow.close();
                myLocationInfowindow = null;
            }
            
            // 버튼 활성화 상태 제거
            locationBtn.classList.remove('active');
            
            console.log('내 위치 마커 제거됨');
            return; // 함수 종료
        }
        
        // 내 위치 마커가 없으면 새로 생성
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const locPosition = new kakao.maps.LatLng(lat, lon);
                
                // 지도를 내 위치로 이동
                map.setCenter(locPosition);
                
                // 새로운 내 위치 마커 생성
                myLocationMarker = new kakao.maps.Marker({
                    position: locPosition,
                    map: map
                });
                
                // 새로운 인포윈도우 생성
                myLocationInfowindow = new kakao.maps.InfoWindow({
                    content: '<div style="padding:8px 12px; font-size:13px; color:#3370ff; font-weight:600;">📍 현재 위치</div>'
                });
                myLocationInfowindow.open(map, myLocationMarker);
                
                // 버튼 활성화 상태 추가
                locationBtn.classList.add('active');
                
                // 5초 후 인포윈도우만 자동 닫기 (마커는 유지)
                setTimeout(function() {
                    if (myLocationInfowindow) {
                        myLocationInfowindow.close();
                    }
                }, 5000);
                
                console.log('내 위치 마커 생성됨');
                
            }, function(error) {
                // 위치 정보 가져오기 실패 시
                let errorMessage = '위치 정보를 가져올 수 없습니다.';
                
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = '위치 정보 접근이 거부되었습니다.\n브라우저 설정에서 위치 권한을 허용해주세요.';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = '위치 정보를 사용할 수 없습니다.';
                        break;
                    case error.TIMEOUT:
                        errorMessage = '위치 정보 요청 시간이 초과되었습니다.';
                        break;
                }
                
                alert(errorMessage);
            }, {
                enableHighAccuracy: true, // 높은 정확도 모드
                timeout: 10000, // 10초 타임아웃
                maximumAge: 0 // 캐시된 위치 사용 안 함
            });
        } else {
            alert('이 브라우저는 위치 정보를 지원하지 않습니다.');
        }
    });
}

// 드롭다운 초기화
function initDropdowns() {
    const sidoSelect = document.getElementById('sido');
    const sigunguSelect = document.getElementById('sigungu');
    const bankSelect = document.getElementById('bank');

    // 시/도 변경 이벤트
    sidoSelect.addEventListener('change', function() {
        const selectedSido = this.value;
        
        // 시/군/구 초기화
        sigunguSelect.innerHTML = '<option value="">시/군/구 선택</option>';
        sigunguSelect.disabled = !selectedSido;
        
        // 은행 초기화
        bankSelect.innerHTML = '<option value="">은행 선택</option>';
        bankSelect.disabled = true;

        if (selectedSido && regionData) {
            // mapInfo에서 선택한 시/도 찾기
            const region = regionData.mapInfo.find(item => item.name === selectedSido);
            
            if (region && region.countries) {
                // 시/군/구 옵션 추가
                region.countries.forEach(country => {
                    const option = document.createElement('option');
                    option.value = country;
                    option.textContent = country;
                    sigunguSelect.appendChild(option);
                });
            }
        }
    });

    // 시/군/구 변경 이벤트
    sigunguSelect.addEventListener('change', function() {
        const selectedSigungu = this.value;
        
        // 은행 초기화
        bankSelect.innerHTML = '<option value="">은행 선택</option>';
        bankSelect.disabled = !selectedSigungu;

        if (selectedSigungu && regionData && regionData.bankInfo) {
            // 은행 옵션 추가 (모든 시/군/구에 동일한 은행 리스트 제공)
            regionData.bankInfo.forEach(bank => {
                const option = document.createElement('option');
                option.value = bank;
                option.textContent = bank;
                bankSelect.appendChild(option);
            });
        }
    });

    // 검색 버튼 클릭 이벤트
    document.getElementById('searchBtn').addEventListener('click', function() {
        const sido = sidoSelect.value;
        const sigungu = sigunguSelect.value;
        const bank = bankSelect.value;

        if (!sido || !sigungu || !bank) {
            alert('지역과 은행을 모두 선택해주세요.');
            return;
        }

        searchBranches(sido, sigungu, bank);
    });
}

// 은행 지점 검색
function searchBranches(sido, sigungu, bank) {
    // 기존 마커 제거
    clearMarkers();

    // 검색 키워드 생성
    const keyword = `${sido} ${sigungu} ${bank}`;
    
    console.log('검색 키워드:', keyword);

    // 카카오 장소 검색 API 사용
    ps.keywordSearch(keyword, function(data, status) {
        if (status === kakao.maps.services.Status.OK) {
            console.log('검색 결과:', data);
            
            // 검색된 장소 위치를 기준으로 지도 범위 재설정
            const bounds = new kakao.maps.LatLngBounds();

            data.forEach(function(place) {
                // 마커 생성
                const markerPosition = new kakao.maps.LatLng(place.y, place.x);
                const marker = new kakao.maps.Marker({
                    position: markerPosition,
                    map: map
                });

                markers.push(marker);
                bounds.extend(markerPosition);

                // 인포윈도우 생성
                const infowindow = new kakao.maps.InfoWindow({
                    content: `
                        <div style="padding:15px; min-width:220px;">
                            <h4 style="margin:0 0 8px 0; font-size:15px; font-weight:600; color:#3370ff;">${place.place_name}</h4>
                            <p style="margin:0 0 5px 0; font-size:13px; color:#666; line-height:1.4;">${place.address_name}</p>
                            ${place.phone ? `<p style="margin:0; font-size:13px; color:#3370ff; font-weight:500;">📞 ${place.phone}</p>` : ''}
                        </div>
                    `
                });

                infowindows.push(infowindow);

                // 마커 클릭 이벤트
                kakao.maps.event.addListener(marker, 'click', function() {
                    // 모든 인포윈도우 닫기
                    infowindows.forEach(iw => iw.close());
                    // 클릭한 마커의 인포윈도우 열기
                    infowindow.open(map, marker);
                });
            });

            // 검색된 위치로 지도 이동
            map.setBounds(bounds);

            if (data.length === 0) {
                alert('검색 결과가 없습니다. 다른 지역이나 은행을 선택해주세요.');
            }
        } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
            alert('검색 결과가 없습니다.');
        } else if (status === kakao.maps.services.Status.ERROR) {
            alert('검색 중 오류가 발생했습니다.');
        }
    });
}

// 마커 제거
function clearMarkers() {
    markers.forEach(marker => marker.setMap(null));
    markers = [];
    
    infowindows.forEach(infowindow => infowindow.close());
    infowindows = [];
}

// 시/도 데이터 로드
function loadSidoOptions() {
    const sidoSelect = document.getElementById('sido');
    
    if (regionData && regionData.mapInfo) {
        regionData.mapInfo.forEach(region => {
            const option = document.createElement('option');
            option.value = region.name;
            option.textContent = region.name;
            sidoSelect.appendChild(option);
        });
    }
}

// 초기화 함수
async function initialize() {
    // 1. data.json 로드
    const dataLoaded = await loadDataJSON();
    
    if (dataLoaded) {
        // 2. 카카오맵 SDK 로드
        loadKakaoMapSDK();
    }
}

// 페이지 로드 시 초기화 시작
window.addEventListener('load', function() {
    initialize();
});