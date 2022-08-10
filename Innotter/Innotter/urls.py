from email.mime import base

from django.contrib import admin
from django.urls import include, path

from pages.urls import urlpatterns as resource_urls
from users.urls import urlpatterns as auth_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include(auth_urls)),
    path("resource/", include(resource_urls)),
]
