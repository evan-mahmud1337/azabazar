from django import urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('account/', include('account.urls')),
    path('api/', include('account.api.urls')),
    path('api/', include('products.api.urls')),
    ] + static(settings.MEDIA_URL, dcoument_root=settings.MEDIA_ROOT)
