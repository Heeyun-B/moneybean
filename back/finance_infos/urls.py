from django.urls import path
from . import views

app_name = 'finances_infos'

urlpatterns = [
    path('', views.info_list, name='info_list'),
    path('info/<int:info_pk>/', views.info_detail, name='info_detail'),
    path('info/<int:info_pk>/comment_create/', views.comment_create, name='comment_create'),
]