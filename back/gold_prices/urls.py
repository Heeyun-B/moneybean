from django.urls import path
from . import views

app_name = "gold_prices"

urlpatterns = [
    path('prices/', views.get_prices, name='get_prices'),
]