from django.http import JsonResponse
from article.models import Article
from article.serializers import ArticleSerializer


# Create your views here.


def article_list(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return JsonResponse(serializer.data, safe=False)
