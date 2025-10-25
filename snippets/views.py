from rest_framework import viewsets
from django.db import transaction

from .models import Snippet
from .serializers import SnippetSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    serializer_class = SnippetSerializer

    def get_queryset(self):
        return Snippet.objects.filter(
            created_by=self.request.user.id
        ).select_related('created_by').prefetch_related('tags')

    def perform_create(self, serializer):
        with transaction.atomic():
            snippet = serializer.save(created_by=self.request.user)
            return snippet
