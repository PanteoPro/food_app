from django.contrib import admin
from django.db.models import ManyToManyField
from django.forms import ModelForm, SelectMultiple, ModelChoiceField
from django.utils.safestring import mark_safe

from .models import *
from .service.admin import (
    get_total_calories_and_weight_from_ingredients,
    get_total_calories_from_calories_and_count_calories,
)


class ChangeTotalCaloriesForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_to_change = []
        if self.fields.get('total_calories', None):
            fields_to_change.append(self.fields['total_calories'])
        if self.fields.get('total_weight', None):
            fields_to_change.append(self.fields['total_weight'])
        for field in fields_to_change:
            field.widget.attrs.update({
                'disabled': True, 'style': 'background: lightgray'
            })
            field.help_text = mark_safe(
                "<span style='color: green; font-size:14px'>Заполнится автоматически</span>"
            )


class RecipeAdminForm(ChangeTotalCaloriesForm):

    def clean(self):
        total_calories = get_total_calories_and_weight_from_ingredients(
            ingredients=self.fields['recipe_ingredients'].queryset
        )[0]
        self.cleaned_data['total_calories'] = total_calories


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    form = RecipeAdminForm
    list_display = ('title', 'time_type', 'cooking_time_format', 'total_calories')


class RecipeIngredientAdminForm(ChangeTotalCaloriesForm):

    def clean(self):
        total_calories = get_total_calories_from_calories_and_count_calories(
            calories=int(self.cleaned_data['ingredient_item'].calories),
            count_grams=int(self.cleaned_data['count_use'])
        )
        self.cleaned_data['total_calories'] = total_calories


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):

    form = RecipeIngredientAdminForm
    list_display = ('ingredient_item', 'recipe', 'count_use', 'total_calories')


class CookIngredientAdminForm(ChangeTotalCaloriesForm):

    def clean(self):
        total_calories = get_total_calories_from_calories_and_count_calories(
            calories=int(self.cleaned_data['ingredient_item'].calories),
            count_grams=int(self.cleaned_data['count_use'])
        )
        self.cleaned_data['total_calories'] = total_calories


@admin.register(CookIngredient)
class CookIngredientAdmin(admin.ModelAdmin):

    form = CookIngredientAdminForm
    list_display = ('ingredient_item', 'cook', 'count_use', 'total_calories')


class CookAdminForm(ChangeTotalCaloriesForm):

    def clean(self):
        total_calories, total_weight = get_total_calories_and_weight_from_ingredients(
            ingredients=self.fields['cook_ingredients'].queryset
        )
        self.cleaned_data['total_calories'] = total_calories
        self.cleaned_data['total_weight'] = total_weight


@admin.register(Cook)
class CookAdmin(admin.ModelAdmin):

    form = CookAdminForm
    list_display = ('recipe', 'total_weight', 'total_calories', 'is_change_count_ingredient')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "cook_ingredients":
            ingredient_item_queryset = IngredientItem.objects.filter(is_ended=False, is_overdue=False)
            cook_ingredient_queryset = CookIngredient.objects.filter(ingredient_item__in=ingredient_item_queryset)
            kwargs['queryset'] = cook_ingredient_queryset
        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Spice)
admin.site.register(PlaceSpice)
admin.site.register(Ingredient)
admin.site.register(IngredientItem)
admin.site.register(CookStage)
admin.site.register(Debt)
