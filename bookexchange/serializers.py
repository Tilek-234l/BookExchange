from rest_framework import serializers
from .models import Book, Comment, Discussion, Review

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = []
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
