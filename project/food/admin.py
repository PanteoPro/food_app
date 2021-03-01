from django.contrib import admin
from django.db.models import ManyToManyField
from django.forms import ModelForm, SelectMultiple, ModelChoiceField
from django.utils.safestring import mark_safe

from .models import *
from .service.admin import (
    get_total_calories_and_weight_from_ingredients,
    get_total_calories_for_ingredient, create_cook_ingredients_from_recipe, add_relations_to_cook,
)


class ChangeTotalCaloriesForm(ModelForm):
    """
        В этой форме, при наличии полей :total_calories, total_weight, меняются атрибуты:
        disabled: True, style: background: lightgray
        Так же добавляется вспомогательный текст к полю
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_to_change = []
        if self.fields.get('total_calories', None):
            fields_to_change.append(self.fields['total_calories'])
        if self.fields.get('total_weight', None):
            fields_to_change.append(self.fields['total_weight'])
        if self.fields.get('all_calories', None):
            fields_to_change.append(self.fields['all_calories'])

        for field in fields_to_change:
            field.widget.attrs.update({
                'disabled': True, 'style': 'background: lightgray'
            })
            field.help_text = mark_safe(
                "<span style='color: green; font-size:14px'>Заполнится автоматически</span>"
            )


class RecipeAdminForm(ChangeTotalCaloriesForm):

    def clean(self):
        """
            Расчитываются каллориии в рецепте при сохранении формы из имеющихся ингредиентов
            Используется QuerySet RecipeIngredients"""
        total_calories = get_total_calories_and_weight_from_ingredients(
            ingredients=self.fields['recipe_ingredients'].queryset
        )
        self.cleaned_data['total_calories'] = total_calories


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    form = RecipeAdminForm
    list_display = ('title', 'time_type', 'cooking_time_format', 'total_calories')


class RecipeIngredientAdminForm(ChangeTotalCaloriesForm):

    def clean(self):
        """Высчитывание и добавление total_calories в форму"""
        total_calories = get_total_calories_for_ingredient(self.cleaned_data)
        self.cleaned_data['total_calories'] = total_calories


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):

    form = RecipeIngredientAdminForm
    list_display = ('ingredient', 'recipe', 'count_use', 'total_calories')


class CookIngredientAdminForm(ChangeTotalCaloriesForm):

    def clean(self):
        """Высчитывание и добавление total_calories в форму"""
        total_calories = get_total_calories_for_ingredient(self.cleaned_data)
        self.cleaned_data['total_calories'] = total_calories


@admin.register(CookIngredient)
class CookIngredientAdmin(admin.ModelAdmin):

    form = CookIngredientAdminForm
    list_display = ('ingredient_item', 'cook', 'count_use', 'total_calories')


class CookAdminForm(ChangeTotalCaloriesForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cook_ingredients = None
        # instance = kwargs.get("instance")
        # if instance:
        #     self.

    def clean(self):
        cleaned_data = super().clean()
        total_calories, total_weight = get_total_calories_and_weight_from_ingredients(
            ingredients=self.cleaned_data['cook_ingredients'],
            weight=True
        )
        self.cleaned_data['total_calories'] = total_calories
        self.cleaned_data['total_weight'] = total_weight


@admin.register(Cook)
class CookAdmin(admin.ModelAdmin):

    form = CookAdminForm
    list_display = ('recipe', 'total_weight', 'total_calories', 'is_change_count_ingredient')

    # def save_model(self, request, obj, form, change):
    #     if form.cook_ingredients:
    #         form.cleaned_data['cook_ingredients'] = form.cook_ingredients
    #
    #     super(CookAdmin, self).save_model(request, obj, form, change)

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
