from django.urls import path
from . import views

app_name = 'finance_news'

urlpatterns = [
    path('news/', views.news_list),
    path('news/<int:news_pk>/', views.news_detail),
    path('news/crawl/', views.crawl_news),
]