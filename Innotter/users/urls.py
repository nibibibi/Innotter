from django.urls import include, path

from .views import LoginView, RefreshTokenView, UserView

urlpatterns = [
    path("user", UserView.as_view()),
    path("login", LoginView.as_view()),
    path("refresh", RefreshTokenView.as_view()),
]
