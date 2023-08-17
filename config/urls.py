from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework.routers import DefaultRouter

from bookexchange import views
from users.views import (CustomUserViewSet,
                         CustomLoginView,
                         CustomLogoutView,
                         CustomPasswordChangeView,
                         CustomRegisterView)

router = DefaultRouter()
router.register(r'custom-users', CustomUserViewSet)

swagger_urlpatterns = [
    path('', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

auth_urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/', include('users.urls')),
]

api_v1_urlpatterns = [
    path('schema/', include(swagger_urlpatterns)),
    path('token/', include(auth_urlpatterns)),
    path('', include(router.urls)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_v1_urlpatterns)),
    path('books/', views.BookList.as_view({'get': 'list', 'post': 'create'}), name='book-list'),
    path('comments/', views.CommentList.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    path('discussions/', views.DiscussionViewSet.as_view({'get': 'list', 'post': 'create'}), name='discussion-list'),
    path('reviews/', views.ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review-list'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password-change'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls
