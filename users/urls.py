from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomLoginView, CustomLogoutView, CustomPasswordChangeView, CustomRegisterView,  # Включите представление
)
from bookexchange.views import BookViewSet, CommentViewSet, DiscussionViewSet, ReviewViewSet, BookCreateAPIView

router = DefaultRouter()

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('book-create/', BookCreateAPIView.as_view({'post': 'create'}), name='book_create'),  # Указываем поддерживаемое действие

    path('', include(router.urls)),
]
