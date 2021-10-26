from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from markdown import Markdown

# Create your models here.


class Tag(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return self.title


class Avatar(models.Model):
    content = models.ImageField(upload_to="avatar/%Y/%m%d")


class Article(models.Model):
    author = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='articles')
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        Tag, blank=True, null=True, related_name='articles')
    avatar = models.ForeignKey(
        Avatar, null=True, blank=True, on_delete=models.SET_NULL, related_name='article'
    )

    def __str__(self):
        return self.title

    def get_md(self):
        md = Markdown(extensions=[
            'markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc', ])
        my_body = md.convert(self.body)
        return my_body, md.toc
