from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """
    Represents a tag for categorizing snippets.

    Fields:
        title (CharField): Unique title for the tag.
    """
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Snippet(models.Model):
    """
    Represents a short text snippet created by a user.

    Fields:
        title (CharField): Title of the snippet.
        note (TextField): The main text content.
        created_by (ForeignKey): The user who created the snippet.
        tags (ManyToManyField): Tags associated with this snippet.
        created_at (DateTimeField): Timestamp when created.
        updated_at (DateTimeField): Timestamp when last updated.
    """
    title = models.CharField(max_length=100)
    note = models.TextField()
    tag = models.ManyToManyField(
        Tag,
        related_name='snippets'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='snippets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
