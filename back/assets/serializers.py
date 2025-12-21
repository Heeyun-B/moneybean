from rest_framework import serializers
from .models import Asset, AssetCategory

class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Asset
        fields = [
            'id', 
            'category',       # 입력받을 때 쓰는 카테고리 ID (ex: 1)
            'category_name',  # 보여줄 때 쓰는 카테고리 이름 (ex: 현금성 자산)
            'name',           # 자산명 (ex: 카카오뱅크)
            'current_value',  # 현재 가치
            'created_at',     # 생성일
            'updated_at',     # 수정일
        ]
        read_only_fields = ('user',)