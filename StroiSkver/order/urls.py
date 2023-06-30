from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path

urlpatterns = [

    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('orders/<int:order_id>/edit/', views.update_order, name='update_order'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('orders/', views.order_list, name='order_list'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('', views.cart, name='cart'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)