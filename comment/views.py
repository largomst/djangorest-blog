
# Create your views here.
from rest_framework import viewsets

from comment.models import Comment
from comment.permissions import IsOwnerOrReadOnly
from comment.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(author=self.request.user)
