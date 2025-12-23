from rest_framework import serializers
from .models import (
    DepositProducts, DepositOptions, DepositSubscription,
    SavingProducts, SavingOptions, SavingSubscription
)


class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = "__all__"


class DepositProductsSerializer(serializers.ModelSerializer):
    options = DepositOptionsSerializer(many=True, read_only=True)
    
    class Meta:
        model = DepositProducts
        fields = "__all__"

class DepositSubscriptionSerializer(serializers.ModelSerializer):
    # 읽기 전용 필드들 (응답에만 포함)
    product_name = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    bank_name = serializers.CharField(source='product.kor_co_nm', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = DepositSubscription
        fields = [
            'id', 
            'user', 
            'user_name',
            'product', 
            'product_name', 
            'bank_name',
            'selected_option', 
            'subscribed_at'
        ]
        read_only_fields = ['user', 'subscribed_at']

class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('product',)


class SavingProductsSerializer(serializers.ModelSerializer):
    options = SavingOptionsSerializer(many=True, read_only=True)
    
    class Meta:
        model = SavingProducts
        fields = '__all__'


class SavingSubscriptionSerializer(serializers.ModelSerializer):
    product = SavingProductsSerializer(read_only=True)
    selected_option = SavingOptionsSerializer(read_only=True)
    
    class Meta:
        model = SavingSubscription
        fields = '__all__'
        read_only_fields = ('user', 'subscribed_at')