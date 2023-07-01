from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path

urlpatterns = [

        path('paper_list/', views.paper_list, name='paper_list'),
        path('edit_paper/<int:paper_id>/', views.edit_paper, name='edit_paper'),
        path('admin/users/', views.user_admin, name='user_admin'),
        path('admin/make_admin/<int:user_id>/', views.make_admin, name='make_admin'),
        path('admin/remove_admin/<int:user_id>/', views.remove_admin, name='remove_admin'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)