from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path

urlpatterns = [

    path('pagematerials/all/', views.product_list, name='materials'),
    path('pagematerials/<slug:category_slug>/', views.category_product_list, name='category_product_list'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)