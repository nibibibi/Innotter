from django.urls import include, path
from rest_framework.routers import DefaultRouter

from pages import views as pages_views
from users import views as users_views

router = DefaultRouter()
router.register(r"users", users_views.UserViewSet, basename="users")
router.register(r"pages", pages_views.PageViewSet, basename="pages")
router.register(r"posts", pages_views.PageViewSet, basename="posts")
router.register(r"tags", pages_views.TagViewSet, basename="tags")

urlpatterns = [
    path("", include(router.urls))
]
