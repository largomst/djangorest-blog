
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from article.models import User

# Create your tests here.


class ArticleTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="foo")
        self.superuser = User.objects.create_superuser(username='bar')

    def test_permission(self):
        url = reverse('article-list')

        # 未登陆可以正常访问
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 未登陆用户不可以修改
        data = {'title': 'foo', 'body': 'bar', }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # superuser 可以修改
        self.client.force_authenticate(self.superuser)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reverse_category(self):
        url = reverse('category-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
