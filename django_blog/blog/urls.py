from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView

app_name = 'blog'

urlpatterns = [
    path('', views.blog_view, name='blog'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='user_profile'),  

    path('post/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('post/<int:post_id>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)