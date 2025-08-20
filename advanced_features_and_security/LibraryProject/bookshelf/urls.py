from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings

app_name = 'bookshelf'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='bookshelf/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='bookshelf/logout.html'), name='logout'),
    path('profile/', views.profile_view, name='profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)