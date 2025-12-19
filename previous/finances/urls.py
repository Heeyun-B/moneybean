from django.urls import path
from . import views

app_name = "finances"

urlpatterns = [
    path(
        "save-deposit-products/",
        views.save_deposit_products,
        name="save_deposit_products",
    ),
    path("deposit-products/", views.deposit_products, name="deposit_products"),
]
