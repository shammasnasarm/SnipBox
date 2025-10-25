from rest_framework import serializers
from .models import Snippet, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class SnippetSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(write_only=True)

    class Meta:
        model = Snippet
        fields = [
            'id', 'title', 'note', 'created_at',
            'updated_at', 'tags', 'created_by'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']

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
