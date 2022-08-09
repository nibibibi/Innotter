from django.contrib import admin
from django.urls import include, path

from users.urls import urlpatterns as auth_views

urlpatterns = [
    path("admin/", admin.site.urls), 
    path("auth/", include(auth_views))
]
