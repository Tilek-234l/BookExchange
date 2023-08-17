from django.shortcuts import render, redirect
from .models import Book, Comment, Discussion, Review
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import BookSerializer, CommentSerializer, DiscussionSerializer, ReviewSerializer

def index(request):
    books = Book.objects.all()
    return render(request, 'bookexchange/index.html', {'books': books})

@login_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        description = request.POST['description']
        cover_image = request.FILES['cover_image']
        owner = request.user
        Book.objects.create(title=title, author=author, description=description, cover_image=cover_image, owner=owner)
        return redirect('index')
    return render(request, 'bookexchange/add_book.html')


class BookList(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CommentList(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
