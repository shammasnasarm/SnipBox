# snippets/tests/test_snippet_api.py

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from snippets.models import Snippet
from snippets.tests.factories import auth_factory, snippet_factory


class SnippetAPITestCase(APITestCase):
    def setUp(self):
        self.user = auth_factory.UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        url = reverse('snippet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_snippet_success(self):
        payload = {
            "title": "New Test Snippet",
            "note": "Testing note",
            "tags": ["python", "drf"]
        }
        url = reverse('snippet-list')
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Test Snippet")
        self.assertEqual(len(response.data['tags']), 2)

    def test_create_snippet_error(self):
        payload = {
        }
        url = reverse('snippet-list')
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertIn('note', response.data)
        self.assertIn('tags', response.data)

    def test_overview_api_success(self):
        snippet_factory.SnippetFactory.create_batch(2, created_by=self.user)
        url = reverse('snippet-overview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_count', response.data)
        self.assertEqual(response.data['total_count'], 2)
        self.assertIsInstance(response.data['snippets'], list)

    def test_retrieve_snippet_success(self):
        snippet = snippet_factory.SnippetFactory(created_by=self.user)
        url = reverse('snippet-detail', args=[snippet.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], snippet.id)

    def tesst_retrive_snippet_not_found(self):
        url = reverse('snippet-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_snippet_success(self):
        snippet = snippet_factory.SnippetFactory(
            created_by=self.user,
            title="Old Title",
            note="Old Note"
        )
        payload = {
            "title": "Updated Title",
            "note": "Updated Note",
            "tags": ["updated", "tags"]
        }
        url = reverse('snippet-detail', args=[snippet.id])
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Title")
        self.assertEqual(len(response.data['tags']), 2)

    def test_delete_snippet_success(self):
        snippet = snippet_factory.SnippetFactory(created_by=self.user)
        snippet_factory.SnippetFactory(created_by=self.user)
        url = reverse('snippet-detail', args=[snippet.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Snippet.objects.filter(id=snippet.id).exists())
        self.assertEqual(len(response.data), 1)


class TagAPITestCase(APITestCase):
    def setUp(self):
        self.user = auth_factory.UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('tag-list')

    def test_list_tags_success(self):
        snippet_factory.TagFactory.create_batch(3)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)

    def test_list_tag_snippets_success(self):
        tag = snippet_factory.TagFactory(title="django")
        tag2 = snippet_factory.TagFactory(title="python")
        snippet1 = snippet_factory.SnippetFactory(created_by=self.user)
        snippet2 = snippet_factory.SnippetFactory(created_by=self.user)
        snippet1.tags.add(tag)
        snippet2.tags.add(tag, tag2)

        url = reverse('tag-snippets', args=[tag.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

        url = reverse('tag-snippets', args=[tag2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
