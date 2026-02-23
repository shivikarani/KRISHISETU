from rest_framework import serializers
from .models import Category, Article

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Article
        fields = ['id', 'title', 'category', 'content', 'media_file', 'created_at']