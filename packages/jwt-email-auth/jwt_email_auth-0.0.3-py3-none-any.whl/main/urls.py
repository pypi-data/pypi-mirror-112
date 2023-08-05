"""'main' project URL Configuration."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

import debug_toolbar
from django_js_reverse.views import urls_js


urlpatterns = [
    path("admin/", admin.site.urls),
    path("js-reverse/", urls_js, name="js-reverse"),
    path("__debug__/", include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
    urlpatterns += path("static/<path:path>", serve, {"document_root": settings.STATIC_ROOT}),
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
