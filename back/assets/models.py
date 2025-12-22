from django.db import models
from django.conf import settings

# 1. 자산 카테고리 (대분류 기능 추가됨)
class AssetCategory(models.Model):
    # 대분류 선택지 정의
    GROUP_CHOICES = (
        ('CASH', '현금성 자산'),
        ('INVEST', '투자 자산'),
        ('DEBT', '부채'),
    )

    name = models.CharField(max_length=50)
    group = models.CharField(max_length=10, choices=GROUP_CHOICES, default='CASH')
    
    description = models.TextField(blank=True)
    icon_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"[{self.get_group_display()}] {self.name}"

# 2. 내 자산 (유저가 입력하는 데이터)
class Asset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assets')
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    current_value = models.DecimalField(max_digits=15, decimal_places=0)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.user.username}] {self.name} - {self.current_value}"
    
# 3. 유저 재정 상태 (월 수입/지출)
class UserFinancialInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='financial_info')
    monthly_income = models.DecimalField(max_digits=12, decimal_places=0, default=0) # 월 수입
    monthly_expense = models.DecimalField(max_digits=12, decimal_places=0, default=0) # 월 지출
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - Income: {self.monthly_income}"