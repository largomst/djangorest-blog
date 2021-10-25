from django.http import Http404

from article.models import Article
from article.permissions import IsAdminUserOrReadOnly
from article.serializers import ArticleSerializer, ArticleDetailSerializer

from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework import generics


# Create your views here.


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminUserOrReadOnly]
