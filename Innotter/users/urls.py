from django.urls import path, include
from .views import UserView, LoginView

urlpatterns = [
    path('user', UserView.as_view()),
    path('login', LoginView.as_view()),
]
