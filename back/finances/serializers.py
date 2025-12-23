from rest_framework import serializers
from .models import Article, Comment

class CommentSeriallizer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'content', 'username', 'article', 'created_at')
        read_only_fields = ('article', 'user')

class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    comments = CommentSeriallizer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(pk=request.user.pk).exists()
        return False
    
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'username', 'comments', 'comment_count', 'like_count', 'is_liked', 'created_at', 'updated_at')        

class ArticleListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'username', 'created_at', 'comment_count', 'like_count')
        

