from datetime import date

from django.db.models import QuerySet

from ..models import Recipe, CookIngredient, Cook, IngredientItem, Debt


def get_total_calories_and_weight_from_ingredients(ingredients: QuerySet, weight=False):
    """
        Из queryset'a CookIngredient или RecipeIngredient считается:
         1) конечное количество каллорий на 100 грамм
         2) конечный вес блюда, если передан флаг weight
        Возвращается dict, под индексом 0 - calories, 1 - weight
    """
    total_calories = calories_sum = weight_sum = 0
    try:
        if len(ingredients):
            for item in ingredients:
                weight_sum += int(item.count_use)
                calories_sum += int(item.total_calories)
            if calories_sum:
                total_calories = calories_sum / weight_sum * 100
            else:
                print("Не смогли считать каллории из ингредиентов")
            if weight:
                return [total_calories, weight_sum]
            return total_calories
        else:
            print("Вы передали пустой Queryset")
    except AttributeError:
        print(
            "Вы передали queryset {}, в котором нет полей count_use и total_calories\n\
            Допустимые классы CookIngredient, RecipeIngredient".format(ingredients[0].__class__)
        )
    if weight:
        return [0, 0]
    return 0


def get_total_calories_for_ingredient(data: dict) -> int:
    """Эта функция высчитывает количество каллорий в ингредиенте"""
    calories = (data.get('ingredient') or data.get('ingredient_item').ingredient).calories
    count_grams = data.get('count_use')
    if calories and count_grams:
        return int(calories * (count_grams/100))


def create_cook_ingredients_from_recipe(recipe: Recipe, cook: Cook) -> list:
    """
        Эта функция создает CookIngredient'ы на основе рецепта
        Возвращает list CookIngredient
    """
    list_cook_ingredients = []
    if not cook.is_change_count_ingredient:
        if len(recipe.recipe_ingredients.all()):
            for recipe_ingredient in recipe.recipe_ingredients.all():
                ingredient = recipe_ingredient.ingredient
                ingredient_item = IngredientItem.objects.filter(ingredient=ingredient)[0]
                count_use = recipe_ingredient.count_use
                total_calories = recipe_ingredient.total_calories
                cook_ingredient_object = CookIngredient.objects.create(
                    ingredient_item=ingredient_item,
                    cook=cook,
                    count_use=count_use,
                    total_calories=total_calories
                )
                list_cook_ingredients.append(cook_ingredient_object)
        else:
            print("Осутствуют ингредиенты")
    else:
        print("Невозможно создать на подобе, стоит True у cook")
    return list_cook_ingredients


def add_relations_to_cook(list_cook_ingredients: list, cook:Cook) -> None:
    for cook_ingredient in list_cook_ingredients:
        cook.cook_ingredients.add(cook_ingredient)
    cook.save()





def check_all_ingredient_items_for_overdue() -> None:
    """Проверка ингредиентов на просрочку"""
    queryset = IngredientItem.objects.filter(is_overdue=False)
    if len(queryset):
        for item in queryset:
            if item.shelf_life < date.today():
                item.is_overdue = True
                item.save()

