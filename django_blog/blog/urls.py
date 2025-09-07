from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView, SearchPostListView, PostsByTagListView
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

    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

     # Tag & search URLs
    path('search/', views.SearchPostListView.as_view(), name='post_search'),
    path('tags/<str:tag_name>/', views.PostsByTagListView.as_view(), name='posts_by_tag'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)