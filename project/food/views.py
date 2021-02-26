from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Recipe, Cook
from .service.admin import create_cook_ingredient_from_recipe, check_all_ingredient_items_for_overdue


class Test(View):

    def get(self, request, *args, **kwargs):
        create_cook_ingredient_from_recipe(Recipe.objects.first(), Cook.objects.first())
        return HttpResponse("Hello")


class Test2(View):

    def get(self, request, *args, **kwargs):
        check_all_ingredient_items_for_overdue()
        return HttpResponse("Hello2")

