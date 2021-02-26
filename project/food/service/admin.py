from datetime import date

from django.db.models import QuerySet

from ..models import Recipe, CookIngredient, Cook, IngredientItem, Debt


def get_total_calories_and_weight_from_ingredients(ingredients: QuerySet) -> list:
    """
        Из queryset'a PlaceIngredient считается:
         1) конечное количество каллорий на 100 грамм
         2) конечный вес блюда
        Возвращается dict, под индексом 0 - calories, 1 - weight
    """
    total_calories = calories_sum = weight_sum = 0
    for item in ingredients:
        weight_sum += int(item.count_use)
        calories_sum += int(item.total_calories)
    if calories_sum:
        total_calories = calories_sum / weight_sum * 100
    return [total_calories, weight_sum]


def get_total_calories_from_calories_and_count_calories(calories: int, count_grams: int) -> int:
    """Эта функция высчитывает количество каллорий в блюде"""
    return int(calories * (count_grams/100))


def create_cook_ingredient_from_recipe(recipe: Recipe, cook: Cook) -> None:
    """Эта функция создает CookIngredient'ы на основе рецепта"""
    if not cook.is_change_count_ingredient:
        if recipe.recipe_ingredients.all():
            for recipe_ingredient in recipe.recipe_ingredients.all():
                ingredient_item = recipe_ingredient.ingredient_item
                count_use = recipe_ingredient.count_use
                total_calories = recipe_ingredient.total_calories
                cook_ingredient_object = CookIngredient.objects.create(
                    ingredient_item=ingredient_item,
                    count_use=count_use,
                    total_calories=total_calories,
                    cook=cook
                )
                cook.cook_ingredients.add(cook_ingredient_object)
        else:
            print("Осутствуют ингредиенты")
    else:
        print("Невозможно создать на подобе, стоит True у cook")


def change_count_from_ingredient_item(cook_ingredient: CookIngredient) -> None:
    """Вычитаем из базы данных, количество текущих ингридиентов"""
    ingredient_item = cook_ingredient.ingredient_item
    count_to_subtract = cook_ingredient.count_use
    result = _change_ingredient_to_ended(ingredient_item, count_to_subtract)
    print(result)
    if result:
        debt = True
        already_ingredients = _get_already_ingredients_by_ingredient_item(ingredient_item)
        if len(already_ingredients):
            for ingredient in already_ingredients:
                result = _change_ingredient_to_ended(ingredient, result)
                if not result:
                    debt = False
                    break

        if debt:
            _create_debt(ingredient_item, result)
            print("Остался долг {}! Добавляем его".format(result))


def _check_ingredient_for_end(ingredient_item: IngredientItem, count_use: int) -> bool:
    """Если мы из IngredientItem вычтем количество в count_use, останется ли положительное число?"""
    result_count = int(ingredient_item.count_now - count_use)
    if result_count > 0:
        return False
    return True


def _change_ingredient_to_ended(ingredient_item: IngredientItem, count_use=0) -> int:
    """
        Меняет у IngredientItem текущее значение в наличии на 0 если не хватает и возвращает непокрытый долг
        иначе просто вычтет значение
    """
    if _check_ingredient_for_end(ingredient_item, count_use):
        result_count = abs(int(ingredient_item.count_now - count_use))
        ingredient_item.count_now = 0
        ingredient_item.is_ended = True
        ingredient_item.save()
        return result_count
    else:
        ingredient_item.count_now = int(ingredient_item.count_now) - int(count_use)
        ingredient_item.save()
        return 0


def _get_already_ingredients_by_ingredient_item(ingredient_item: IngredientItem) -> QuerySet:
    """Возвращает QuerySet объектов IngredientItem по ingredient, которые еще не закончились и не просрочились"""
    return IngredientItem.objects.filter(ingredient=ingredient_item.ingredient, is_ended=False, is_overdue=False)


def _create_debt(ingredient_item: IngredientItem, count: int) -> None:
    Debt.objects.create(
        ingredient=ingredient_item.ingredient,
        count=count
    )


def check_all_ingredient_items_for_overdue() -> None:
    """Проверка ингредиентов на просрочку"""
    queryset = IngredientItem.objects.filter(is_overdue=False)
    if len(queryset):
        for item in queryset:
            if item.shelf_life < date.today():
                item.is_overdue = True
                item.save()

