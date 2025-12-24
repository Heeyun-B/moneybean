from django.urls import path
from . import views

app_name = "ais"

urlpatterns = [
    path('diagnosis/', views.diagnosis, name='diagnosis'),
    path('luck/', views.luck, name='luck'),
]
