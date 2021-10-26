from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.title
