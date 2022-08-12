from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import page_views, posts_views, tag_views, user_views

router = DefaultRouter()
router.register(r"users", user_views.UserViewSet, basename="users")
router.register(r"pages", page_views.PageViewSet, basename="pages")
router.register(r"posts", posts_views.PostViewSet, basename="posts")
router.register(r"tags", tag_views.TagViewSet, basename="tags")

urlpatterns = [path("", include(router.urls))]
