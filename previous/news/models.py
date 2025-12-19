from django.db import models


# Create your models here.
class News(models.Model):
    title = models.TextField(max_length=200)
    link = models.TextField(max_length=200)
    description = models.TextField(max_length=200)
    is_bookmarked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
