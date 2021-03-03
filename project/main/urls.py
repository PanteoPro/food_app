from django.urls import path

from .views import (
    RegisterView, LoginView, LogoutView, ProfileView,
    ProfileSettingsView, ProfileSettingsApplyView, EatCookView,
    EatCookAddView, EatIngredientView, EatIngredientAddView
)

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("profile_settings/", ProfileSettingsView.as_view(), name="profile_settings"),
    path("profile_settings_apply/", ProfileSettingsApplyView.as_view(), name="profile_settings_apply"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("eat_cook/", EatCookView.as_view(), name="eat_cook"),
    path("eat_cook_add/", EatCookAddView.as_view(), name="eat_cook_add"),
    path("eat_ingredient_item/", EatIngredientView.as_view(), name="eat_ingredient_item"),
    path("eat_ingredient_item_add/", EatIngredientAddView.as_view(), name="eat_ingredient_item_add"),
]