from django.urls import path
from . import views

app_name = "ais"

urlpatterns = [
    path('diagnosis/', views.diagnosis, name='diagnosis'),
    path('recommend/', views.recommend_products, name='recommend_products'),
    path('luck/', views.luck, name='luck'),
]
