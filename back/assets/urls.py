from django.urls import path
from . import views

urlpatterns = [
    # 카테고리 정보 (ex: 주식, 코인, 현금)
    path('categories/', views.AssetCategoryListView.as_view(), name='category-list'),
    
    # 자산 조회 및 추가 (GET, POST)
    path('my-assets/', views.AssetListCreateView.as_view(), name='asset-list-create'),
    
    # 특정 자산 수정 및 삭제 (PUT, DELETE)
    path('my-assets/<int:pk>/', views.AssetDetailView.as_view(), name='asset-detail'),

    path('financial-info/', views.UserFinancialInfoView.as_view(), name='financial-info'),
]