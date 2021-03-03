from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from .forms import IngredientItemForm, RecipeForm, CookForm
from .models import Recipe, Ingredient, Spice, Cook

from .service.views import create_ingredient_item, create_recipe, create_cook
from config.service.views import set_model_all_in_context

"""
    Что должно быть:
    1) Добавление через сайт
        1.1) Рецепт
            1.1.1) Добавлять этапы
            1.1.2) Ингредииенты для рецепта
        1.2) Блюда
            1.2.1) Ингредиенты для блюда, если отличается от рецепта
        1.3) IngredientItem
    2) Отображение рецептов
    3) Рандомный рецепт на завтра, обед, ужин, перекус
    4) Автоматическая проверка на просрочку
    5) Автоматичскаая проверка закончился продукт или нет
"""


class MainView(View):
    """Отображение главной страницы приложения"""

    def get(self, request, *args, **kwargs):
        return render(request, 'food_main.html')


class IngredientItemView(View):
    """Отображение страницы с добавление ингредиента на склад"""

    def get(self, request, *args, **kwargs):
        form = IngredientItemForm()
        context = dict()
        context['form'] = form
        return render(request, 'ingredient_item.html', context=context)


class IngredientItemAddView(View):
    """Добавление ингредиента на склад"""

    def post(self, request, *args, **kwargs):

        form = IngredientItemForm(request.POST)
        if form.is_valid():
            result = create_ingredient_item(form)
            for message in result["messages"]:
                messages.add_message(request, messages.INFO, "{}".format(message))
        return redirect('/ingredient_item')


class RecipeListView(ListView):
    """Вывод всех рецептов"""

    model = Recipe


class RecipeView(View):
    """Отображение страницы добавления рецепта"""

    def get(self, request, *args, **kwargs):
        form = RecipeForm()
        context = dict()
        context['form'] = form
        set_model_all_in_context(Ingredient, context, "id", "title")
        set_model_all_in_context(Spice, context, "id", "title")
        return render(request, "recipe.html", context=context)


class RecipeAddView(View):
    """Добавление рецепта"""

    def post(self, request, *args, **kwargs):
        result = create_recipe(request.POST)
        if result['success']:
            messages.add_message(request, messages.INFO, "Рецепт {} успешно добавлен".format(result['messages'][0]))
        else:
            for message in result["messages"]:
                messages.add_message(request, messages.ERROR, "{}".format(message))

        return redirect('/recipe')


class CookListView(ListView):
    """Вывод всех блюд"""

    model = Cook


class CookView(View):
    """Отображение страницы добавления блюда"""

    def get(self, request, *args, **kwargs):
        form = CookForm()
        context = dict()
        context['form'] = form
        set_model_all_in_context(Recipe, context)
        return render(request, "cook.html", context=context)


class CookAddView(View):
    """Добавление блюда"""

    def post(self, request, *args, **kwargs):
        result = create_cook(request.POST)
        if result['success']:
            messages.add_message(request, messages.INFO, "Блюдо {} успешно добавлено".format(result['messages'][0]))
        else:
            for message in result["messages"]:
                messages.add_message(request, messages.ERROR, "{}".format(message))
        return redirect("/cook")
