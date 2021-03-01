from django.urls import path

from .views import (
    IngredientItemView,
    IngredientItemAddView,
    MainView,
    RecipeView,
    RecipeAddView,
    CookView,
    CookAddView
)

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("ingredient_item/", IngredientItemView.as_view(), name="ingredient_item"),
    path("ingredient_item_add/", IngredientItemAddView.as_view(), name="ingredient_item_add"),
    path("recipe/", RecipeView.as_view(), name="recipe"),
    path("recipe_add/", RecipeAddView.as_view(), name="recipe_add"),
    path("cook/", CookView.as_view(), name="cook"),
    path("cook_add/", CookAddView.as_view(), name="cook_add"),
]