from rest_framework import serializers
from .models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'username', 'created_at', 'updated_at')
        # user는 제외
        

class ArticleListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'username', 'created_at')
        

class CommentSeriallizer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'content', 'username', 'article', 'created_at')
        read_only_fields = ('article', 'user')