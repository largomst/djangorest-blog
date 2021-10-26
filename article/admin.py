from nntplib import ArticleInfo
from django.contrib import admin

from article.models import Article, Avatar, Category, Tag

# Register your models here.

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Avatar)
