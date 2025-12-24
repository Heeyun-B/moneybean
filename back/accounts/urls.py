from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_info, name='user_info'),
    path('check-id/<str:username>/', views.check_id),
    path('check-nickname/<str:nickname>/', views.check_nickname),
    
    path('profile/', views.profile),                    # 프로필 조회
    path('profile/update/', views.profile_update),      # 프로필 수정
    path('profile/password/', views.change_password),   # 비밀번호 변경
    path('profile/delete/', views.profile_delete),      # 회원 탈퇴
    path('profile/image/delete/', views.delete_profile_image),  # 이미지 삭제
]