from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/', views.profile, name='profile'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)