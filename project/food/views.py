from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from .forms import IngredientItemForm, RecipeForm, CookForm
from .models import Recipe, Ingredient, Spice, Cook
from .service.models import create_recipe, create_cook, create_ingredient_item
from .service.views import set_model_in_context

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


# class Test2(View):
#
#     def get(self, request, *args, **kwargs):
#         check_all_ingredient_items_for_overdue()
#         return HttpResponse("Hello2")


class MainView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'food_main.html')


class IngredientItemView(View):

    def get(self, request, *args, **kwargs):
        form = IngredientItemForm()
        context = dict()
        context['form'] = form
        return render(request, 'ingredient_item.html', context=context)


class IngredientItemAddView(View):

    def post(self, request, *args, **kwargs):

        form = IngredientItemForm(request.POST)
        if form.is_valid():
            result = create_ingredient_item(form)
            for message in result["messages"]:
                messages.add_message(request, messages.INFO, "{}".format(message))
        return redirect('/ingredient_item')


class RecipeListView(ListView):

    model = Recipe


class RecipeView(View):

    def get(self, request, *args, **kwargs):
        form = RecipeForm()
        context = dict()
        context['form'] = form
        set_model_in_context(Ingredient, context, "id", "title")
        set_model_in_context(Spice, context, "id", "title")
        return render(request, "recipe.html", context=context)


class RecipeAddView(View):

    def post(self, request, *args, **kwargs):
        result = create_recipe(request.POST)
        if result['success']:
            messages.add_message(request, messages.INFO, "Рецепт {} успешно добавлен".format(result['messages'][0]))
        else:
            for message in result["messages"]:
                messages.add_message(request, messages.ERROR, "{}".format(message))

        return redirect('/recipe')


class CookListView(ListView):

    model = Cook


class CookView(View):

    def get(self, request, *args, **kwargs):
        form = CookForm()
        context = dict()
        context['form'] = form
        set_model_in_context(Recipe, context)
        return render(request, "cook.html", context=context)


class CookAddView(View):

    def post(self, request, *args, **kwargs):
        result = create_cook(request.POST)
        if result['success']:
            messages.add_message(request, messages.INFO, "Блюдо {} успешно добавлено".format(result['messages'][0]))
        else:
            for message in result["messages"]:
                messages.add_message(request, messages.ERROR, "{}".format(message))
        return redirect("/cook")
