from django.contrib import admin
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from .models import *
from .service.admin import (
    get_total_calories_from_ingredients,
    get_total_calories_from_calories_and_count_calories
)


class AutoFieldFillForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total_calories'].widget.attrs.update({
            'disabled': True, 'style': 'background: lightgray'
        })
        self.fields['total_calories'].help_text = mark_safe(
            "<span style='color: green; font-size:14px'>Заполнится автоматически</span>"
        )


class FoodAdminForm(AutoFieldFillForm):

    def clean(self):
        total_calories = get_total_calories_from_ingredients(ingredients=self.fields['ingredient_items'].queryset)
        self.cleaned_data['total_calories'] = total_calories


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):

    form = FoodAdminForm
    list_display = ('title', 'time_type', 'cooking_time_format', 'total_calories')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(db_field)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PlaceIngredientAdminForm(AutoFieldFillForm):

    def clean(self):
        total_calories = get_total_calories_from_calories_and_count_calories(
            calories=int(self.cleaned_data['ingredient_item'].calories),
            count_gramms=int(self.cleaned_data['count_use'])
        )
        self.cleaned_data['total_calories'] = total_calories


@admin.register(PlaceIngredient)
class PlaceIngredientAdmin(admin.ModelAdmin):

    form = PlaceIngredientAdminForm


admin.site.register(Spice)
admin.site.register(PlaceSpice)
admin.site.register(Ingredient)
admin.site.register(IngredientItem)
admin.site.register(CookStage)
