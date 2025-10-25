from rest_framework import serializers
from .models import Snippet, Tag


class SnippetSerializer(serializers.ModelSerializer):
    """
    Serialize Snippet model data for CRUD operations.

    Used in:
    - SnippetViewSet for create, retrieve, update, and destroy actions.

    Fields:
    - id: Unique identifier of the snippet.
    - title: Title of the snippet.
    - note: The main text content of the snippet.
    - created_at (datetime): Timestamp when the record was created (read-only)
    - updated_at (datetime): Timestamp when the record was last updated
        (read-only)
    - tags (list): List of tag titles.

    """
    tags = serializers.ListField(write_only=True)

    class Meta:
        model = Snippet
        fields = [
            'id', 'title', 'note', 'created_at',
            'updated_at', 'tags',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        snippet = Snippet.objects.create(**validated_data)

        for tag_title in tags_data:
            tag, _ = Tag.objects.get_or_create(title=tag_title)
            snippet.tags.add(tag)
        return snippet

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data is not None:
            tag_objects = []
            for tag_title in tags_data:
                tag, _ = Tag.objects.get_or_create(title=tag_title)
                tag_objects.append(tag)
            instance.tags.set(tag_objects)

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = list(
            instance.tags.values_list('title', flat=True)
        )
        return representation


class SnippetOverviewSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for snippet overview.

    Used in:
    - SnippetViewSet overview action.

    Fields:
    - id: Unique identifier of the snippet.
    - title: Title of the snippet.
    - url: Hyperlinked URL to the snippet detail view.
    """
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'url']
        extra_kwargs = {
            'url': {'view_name': 'snippet-detail', 'lookup_field': 'pk'}
        }
