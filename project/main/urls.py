from django.urls import path

from .views import MainView, RegisterView, LoginView, LogoutView

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]