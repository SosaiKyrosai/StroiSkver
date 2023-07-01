from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeDoneView, PasswordChangeView
urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add_question/', views.add_question, name='add_question'),
    path('reset_password_request/', views.reset_password_request, name='reset_password_request'),
    path('account/reset_password_confirm/<str:username>/', views.reset_password_confirm, name='reset_password_confirm'),
    path('password_reset_success/', views.password_reset_success, name='password_reset_success'),
    path ('password_change/done/', PasswordChangeDoneView.as_view (template_name='password_change_done.html'),name='password_change_done'),
    path ('password_change/', PasswordChangeView.as_view (template_name='password_change.html'),name='password_change'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)