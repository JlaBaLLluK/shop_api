from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/registration/', include('registration.urls')),
    path('api/authorization/', include('authorization.urls')),
    path('api/user/', include('user.urls')),
    path('api/profile_settings/', include('profile_settings.urls')),
    path('api/sale_advertisement/', include('sale_advertisement.urls')),
    path('api/favourite_advertisements/', include('favourite_advertisements.urls'))
]
