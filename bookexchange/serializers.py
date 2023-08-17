from rest_framework import serializers
from .models import Book, Comment, Discussion, Review
from django.conf import settings
from django.contrib.auth.models import User

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
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