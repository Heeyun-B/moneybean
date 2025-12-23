from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('articles/<int:article_pk>/', views.article_detail, name='article_detail'),
    path('articles/<int:article_pk>/comment_create/', views.comment_create, name='comment_create'),
    path('info/<int:article_pk>/like/', views.like_article),
]