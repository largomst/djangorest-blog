from rest_framework import serializers


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(allow_blank=False, max_length=100)
    body = serializers.CharField(allow_blank=True)
    created = serializers.UniqueForDateValidator
    updated = serializers.UniqueForDateValidator
