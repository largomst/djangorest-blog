from django.forms import fields
from rest_framework import serializers

from article.models import Article, Avatar, Category, Tag
from user_info.serializers import UserDescSerializer
from comment.serializers import CommentSerializer


class ArticleListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="article:detail")
    author = UserDescSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'created', 'author', 'url'
        ]
        read_only_fields = ['author']


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fileds = ['created']


class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    """用于在 Category 显示简要信息的 Article 序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        fields = ['url', 'title']


class CategoryDetailSerializer(serializers.ModelSerializer):
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'created', 'articles']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    def check_tag_obj_exists(self, validated_data):
        """避免创建重复的 tag"""
        title = validated_data.get('title')
        if Tag.objects.filter(title=title).exists():
            raise serializers.ValidationError(f'Tag with title {title} exist.')

    def create(self, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().create(validated_data)

    def updated(self, instance, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Tag
        fields = '__all__'


class AvatarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='avatar-detail')

    class Meta:
        model = Avatar
        fields = '__all__'


class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    author = UserDescSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(
        write_only=True, allow_null=True, required=True)
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(), many=True, required=False, slug_field='title')
    avatar = AvatarSerializer(read_only=True)
    avatar_id = serializers.IntegerField(
        write_only=True,
        allow_null=True,
        required=False
    )

    def validate_category_id(self, value):
        """确保传入有效的 category id"""
        if Category.objects.filter(id=value).exists() and value is not None:
            raise serializers.ValidationError(
                f'Category with id {value} not exists')
        return value

    def to_internal_value(self, data):
        """创建不存在的标签"""
        tags_data = data.get('tags')
        if isinstance(tags_data, list):
            for title in tags_data:
                if not Tag.objects.filter(title=title).exists():
                    Tag.objects.create(title=title)
        return super().to_internal_value(data)

    def validate_avatar_id(self, value):
        if not Avatar.objects.filter(id=value).exists() and value is not None:
            raise serializers.ValidationError(
                f'Avatar with id {value} not exists.')
        return value


class ArticleSerializer(ArticleBaseSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {
            'body': {'write_only': True}
        }


class ArticleDetailSerializer(ArticleBaseSerializer):
    body_html = serializers.SerializerMethodField()
    toc_html = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    def get_body_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'
