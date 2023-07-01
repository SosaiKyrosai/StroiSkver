from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path

urlpatterns = [

    path('plaster_calc/', views.plaster_calc, name='plaster_calc'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)