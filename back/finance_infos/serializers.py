from rest_framework import serializers
from .models import ArticleInfo, CommentInfo

class ArticleInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ArticleInfo
        fields = ('id', 'title', 'content', 'username', 'created_at', 'updated_at')
        # user는 제외
        

class ArticleInfoListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ArticleInfo
        fields = ('id', 'title', 'content', 'username', 'created_at')
        

class CommentInfoSeriallizer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = CommentInfo
        fields = ('id', 'content', 'username', 'article', 'created_at')
        read_only_fields = ('article', 'user')