from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CommentViewSet, DiscussionViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'discussions', DiscussionViewSet, basename='discussion')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('api/', include(router.urls)),

]
