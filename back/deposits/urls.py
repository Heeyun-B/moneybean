from django.urls import path
from . import views

app_name = "deposits"

urlpatterns = [
    path(
        "save-deposit-products/",
        views.save_deposit_products,
        name="save_deposit_products",
    ),
    path("deposit-products/", views.deposit_products, name="deposit_products"),
    path('deposit-products/<str:fin_prdt_cd>/', views.deposit_product_detail),
    path('deposit-products/<str:fin_prdt_cd>/subscribe/', views.subscribe_product, name='subscribe_product'),
    path('deposit-products/<str:fin_prdt_cd>/unsubscribe/', views.unsubscribe_product, name='unsubscribe_product'),
    path('my-subscriptions/', views.my_subscriptions, name='my_subscriptions'),
]
