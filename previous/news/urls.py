from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch-news/', views.fetch_news, name='fetch_news'),
    path('view-all/', views.view_all_news, name='view_all_news'),
    path('bookmarked/', views.view_bookmarked_news, name='view_bookmarked_news'),
    path('detail/<int:news_id>/', views.news_detail, name='news_detail'),
    path('bookmark/<int:news_id>/', views.toggle_bookmark, name='toggle_bookmark'),
]
