from django.urls import path

from .views import Test, Test2

urlpatterns = [
    path("", Test.as_view(), name="test"),
    path("1", Test2.as_view(), name="test2")
]