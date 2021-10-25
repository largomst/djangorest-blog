from django.http import Http404

from article.models import Article
from article.permissions import IsAdminUserOrReadOnly
from article.serializers import ArticleListSerializer, ArticleDetailSerializer, ArticleSerializer

from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
