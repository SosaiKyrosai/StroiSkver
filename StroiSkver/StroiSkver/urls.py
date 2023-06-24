from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('account/', include('Account.urls')),
    path('admin/', admin.site.urls),
    path('buildingmaterials/', include('Buildingmaterials.urls')),
    path('', include('Home.urls')),
]

