from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookList, basename='book')
router.register(r'comments', views.CommentList, basename='comment')
router.register(r'discussions', views.DiscussionViewSet, basename='discussion')
router.register(r'reviews', views.ReviewViewSet, basename='review')

urlpatterns = [
    path('', views.index, name='index'),
    path('add_book/', views.add_book, name='add_book'),
    path('api/', include(router.urls)),
]

