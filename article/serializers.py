from unicodedata import category
from django.forms import fields
from rest_framework import serializers

from article.models import Article, Category
from user_info.serializers import UserDescSerializer


class ArticleListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="article:detail")
    author = UserDescSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'created', 'author', 'url'
        ]
        read_only_fields = ['author']


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fileds = ['created']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserDescSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(
        write_only=True, allow_null=True, required=True)

    def validate_category_id(self, value):
        if Category.objects.filter(id=value).exists():
            return value
        else:
            raise serializers.ValidationError(
                f'Category with id {value} not exists')

    class Meta:
        model = Article
        fields = '__all__'
        ordering = ['-created']
