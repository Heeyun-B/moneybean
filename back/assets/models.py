from django.db import models
from django.conf import settings

class AssetCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assets')
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    current_value = models.DecimalField(max_digits=15, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.user.username}] {self.name} - {self.current_value}"