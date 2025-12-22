from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Asset, AssetCategory
from .serializers import AssetSerializer, AssetCategorySerializer

class AssetCategoryListView(generics.ListAPIView):
    """
    자산 카테고리 목록 조회 (Dropdown 메뉴 구성용)
    """
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    permission_classes = [IsAuthenticated]


class AssetListCreateView(generics.ListCreateAPIView):
    """
    내 자산 목록 조회 및 생성
    GET: 로그인한 유저의 자산 리스트 반환
    POST: 새로운 자산 정보 등록
    """
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 로그인한 유저의 데이터만 필터링하여 반환 (보안 필수)
        return Asset.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 데이터 저장 시 user 필드에 현재 요청한 유저를 자동으로 할당
        serializer.save(user=self.request.user)


class AssetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    특정 자산 상세 조회, 수정, 삭제
    URL parameter: pk (asset_id)
    """
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 본인의 자산에만 접근 가능하도록 쿼리셋 제한 (IDOR 방지)
        return Asset.objects.filter(user=self.request.user)