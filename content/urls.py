# content/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .views import PostListAPIView, PostPageView, notification_view, upload_document, document_list

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
    path('', views.home, name='home'),  # or any other view
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('create_post/', views.create_post, name='create_post'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.post_update, name='post_update'),
    path('<int:pk>/delete/', views.post_delete, name = 'post_delete'),
    path('register/', views.register_view, name = 'register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.my_profile, name='profile'),
    path('posts/', views.blog_filter_view, name='post-filter'),
    path('api/api_posts/', PostListAPIView.as_view(), name='api-posts'),
    path('ajax_posts/', PostPageView.as_view(), name='posts-page'),
    path('api/', include(router.urls)),
    path('api/token-auth/', obtain_auth_token),
    path('api/jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('notifications/', notification_view, name='notifications'),
    path('upload/', upload_document, name='upload-document'),
    path('document-list/', document_list, name='document-list'),

]