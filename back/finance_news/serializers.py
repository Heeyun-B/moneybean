from rest_framework import serializers
from .models import NewsArticle

class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = '__all__'

class NewsArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = ('id', 'title', 'press', 'published_date', 'link', 'content')