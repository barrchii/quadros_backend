from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/cart/', include('cart.urls')),
    re_path(r'^(?P<path>.+)$', serve, {
        'document_root': settings.STATICFILES_DIRS[0],
    }),
]