from rest_framework import serializers
from .models import Article, Comment

class CommentSeriallizer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.nickname', read_only=True)
    user_profile_image = serializers.SerializerMethodField()

    def get_user_profile_image(self, obj):
        if obj.user.profile_image and hasattr(obj.user.profile_image, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.user.profile_image.url)
            return obj.user.profile_image.url
        return None

    class Meta:
        model = Comment
        fields = ('id', 'content', 'username', 'user_profile_image', 'article', 'created_at')
        read_only_fields = ('article', 'user')

class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.nickname', read_only=True)
    user_profile_image = serializers.SerializerMethodField()
    comments = CommentSeriallizer(source='comment_set', many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    def get_user_profile_image(self, obj):
        if obj.user.profile_image and hasattr(obj.user.profile_image, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.user.profile_image.url)
            return obj.user.profile_image.url
        return None

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(pk=request.user.pk).exists()
        return False

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'username', 'user_profile_image', 'comments', 'comment_count', 'like_count', 'is_liked', 'created_at', 'updated_at')        

class ArticleListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.nickname', read_only=True)
    user_profile_image = serializers.SerializerMethodField()
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)

    def get_user_profile_image(self, obj):
        if obj.user.profile_image and hasattr(obj.user.profile_image, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.user.profile_image.url)
            return obj.user.profile_image.url
        return None

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'username', 'user_profile_image', 'created_at', 'comment_count', 'like_count')