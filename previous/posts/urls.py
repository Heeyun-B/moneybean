from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<int:post_pk>/", views.detail, name="detail"),
    path("create/", views.create, name="create"),
    path("update/<int:post_pk>/", views.update, name="update"),
    path("delete/<int:post_pk>/", views.delete, name="delete"),
    path(
        "comments_create/<int:post_pk>/", views.comments_create, name="comments_create"
    ),
    path(
        "comments_delete/<int:post_pk>/<int:comment_pk>",
        views.comments_delete,
        name="comments_delete",
    ),
]
