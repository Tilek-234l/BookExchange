import os

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile

from bookexchange.models import Book, Comment, Discussion, Review
from bookexchange.serializers import CommentSerializer, BookSerializer

class BookTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book_data = {
            'title': 'Sample Book',
            'author': 'John Doe',
            'description': 'Sample description',
            'owner': self.user,
        }
        self.book = Book.objects.create(**self.book_data)

    import os
    from django.core.files.uploadedfile import SimpleUploadedFile

    # ... (оставьте остальной код без изменений)

    def test_create_book(self):
        url = reverse('book-list')
        self.client.login(username='admin', password='admin')

        cover_image_path = os.path.join(os.path.dirname(__file__), 'media', 'book_covers', 'maxresdefault.jpg')

        with open(cover_image_path, 'rb') as img_file:
            book_data = {
                'title': 'Sample Book 2',
                'author': 'John Doe',
                'description': 'Sample description',
                'owner': self.user.id,
            }
            response = self.client.post(url, data=book_data, format='multipart',
                                        HTTP_CONTENT_DISPOSITION='attachment; filename=cover.jpg', file=img_file)

            if response.status_code != status.HTTP_201_CREATED:
                print(response.data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_book_list(self):
        url = reverse('book-list')
        # Create another book
        Book.objects.create(title='Sample Book 2', author='John Doe', description='Sample description', owner=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Now there are 2 books in the list

    def test_get_book_detail(self):
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        updated_data = {'title': 'Updated Title', 'author': 'Updated Author', 'description': 'Updated Description'}
        self.client.login(username='testuser', password='testpassword')
        response = self.client.patch(url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')
        self.assertEqual(self.book.author, 'Updated Author')
        self.assertEqual(self.book.description, 'Updated Description')

    def test_delete_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)  # Assuming there's 0 book left after deletion

# ... Similar tests for Comment, Discussion, and Review ...

class BookSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_valid_serializer(self):
        data = {
            'title': 'Sample Title',
            'author': 'Sample Author',
            'description': 'Sample Description',
            'owner': self.user.id,  # Use user.id instead of user
            'cover_image': SimpleUploadedFile(
                name='maxresdefault.jpg',
                content=b'',
                content_type='image/jpeg'
            )
        }
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        print(serializer.errors)

    def test_invalid_serializer(self):
        data = {'title': '', 'author': 'Sample Author', 'description': 'Sample Description'}
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())

# ... Similar tests for CommentSerializer, DiscussionSerializer, and ReviewSerializer ...

class CommentSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(title='Sample Book', author='John Doe', description='Sample description', owner=self.user)

    def test_valid_serializer(self):
        discussion = Discussion.objects.create(title='Sample Discussion', creator=self.user, book=self.book)
        data = {'text': 'Sample comment', 'user': self.user.id, 'discussion': discussion.id, 'book': self.book.id}
        serializer = CommentSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self):
        discussion = Discussion.objects.create(title='Sample Discussion', creator=self.user, book=self.book)
        data = {'text': 'Sample comment', 'user': self.user.id + 1, 'discussion': discussion.id, 'book': self.book.id}
        serializer = CommentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
