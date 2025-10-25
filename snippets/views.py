from rest_framework import viewsets
from django.db import transaction
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
)

from .models import Snippet, Tag
from .serializers import (
    SnippetSerializer, SnippetOverviewSerializer, TagSerializer
)


class SnippetViewSet(
    viewsets.ViewSet,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
):
    """
    ViewSet for managing user snippets.

    overview: Returns total_snippets and snippets with title and url
        to its details which are created by the authenticated user.
    create: Creates a new snippet and get_or_create tags and links it.
    retrieve: Returns snippet details.
    update: Updates snippet data.
    destroy: Deletes snippet and returns updated list.
    """
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Snippet.objects.filter(
            created_by=self.request.user.id
        ).select_related('created_by').prefetch_related('tags')

    def perform_create(self, serializer):
        with transaction.atomic():
            snippet = serializer.save(created_by=self.request.user)
            return snippet

    @action(detail=False, methods=['get'], url_path='overview')
    def overview(self, request, *args, **kwargs):
        snippets = self.get_queryset()
        serializer = SnippetOverviewSerializer(
            snippets,
            many=True,
            context={'request': request}
        )
        return Response({
            "total_count": snippets.count(),
            "snippets": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        snippets = self.get_queryset()
        serializer = self.get_serializer(snippets, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ViewSet, ListAPIView):
    """
    ViewSet for listing tags and retrieving snippets by tag.

    list: Returns all tags.
    snippets: Returns snippets associated with the tag created by the
        authenticated user.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def snippets(self, request, pk=None):
        tag = self.get_object()
        snippets = tag.snippets.filter(created_by=request.user)
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
