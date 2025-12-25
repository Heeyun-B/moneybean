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
    path('my-subscriptions-deposit/', views.my_subscriptions_deposit, name='my_subscriptions_deposit'),

    path('save-saving-products/', views.save_saving_products),
    path('saving-products/', views.saving_products),
    path('saving-products/<str:fin_prdt_cd>/', views.saving_product_detail),
    path('saving-products/<str:fin_prdt_cd>/subscribe/', views.subscribe_saving),
    path('saving-products/<str:fin_prdt_cd>/unsubscribe/', views.unsubscribe_saving),
    path('my-subscriptions-saving/', views.my_subscriptions_saving),
]
