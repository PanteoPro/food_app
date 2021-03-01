from django.forms import ModelForm, DateInput

from .models import IngredientItem, Recipe, Cook


class IngredientItemForm(ModelForm):

    class Meta:
        model = IngredientItem
        fields = ('ingredient', 'count_start', 'count_now', 'manufacturer', 'shelf_life')
        widgets = {
            "shelf_life": DateInput(attrs={"type": "date"})
        }


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'time_type', 'cooking_time',)


class CookForm(ModelForm):

    class Meta:
        model = Cook
        fields = ("recipe", "is_change_count_ingredient")
        help_texts = {
            "is_change_count_ingredient": "Если оставите поле пустым, то количество ингредиентов возьмется из рецепта"
        }
