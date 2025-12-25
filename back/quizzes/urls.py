from django.urls import path
from . import views

urlpatterns = [
    path('today/', views.TodayQuizView.as_view()),
    path('attendance/', views.AttendanceView.as_view()),
]