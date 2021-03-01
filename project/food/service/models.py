from .essential import subtraction_from_store, set_information_of_totals
from .post_manager import create_objects_from_post, renaming_kwargs_from_list
from ..models import Recipe, RecipeIngredient, Cook, IngredientItem, Debt


def create_ingredient_item(form):
    ingredient_item = form.save(commit=False)

    check_debt(ingredient_item)


def check_debt(ingredient_item: IngredientItem) -> None:
    """Проверяет есть ли долги до данному ингредиенту, и если есть за оплатить по долгам"""
    ingredient = ingredient_item.ingredient
    debts = Debt.objects.filter(ingredient=ingredient, is_paid_of=False)
    count_now = ingredient_item.count_now
    is_all_redeemed = True

    if len(debts):
        for debt in debts:
            count_debt = debt.count
            count_now -= count_debt
            if count_now <= 0:
                is_all_redeemed = False
                if count_now < 0:
                    debt.count = abs(count_now)
                else:
                    debt.count = 0
                    debt.is_paid_of = True
                debt.save()
                ingredient_item.count_now = 0
                ingredient_item.is_ended = True
                ingredient_item.save()
                break
            else:
                debt.count = 0
                debt.is_paid_of = True
                debt.save()

    if is_all_redeemed:
        ingredient_item.count_now = count_now
        ingredient_item.save()


def create_recipe(data):
    """
        Последовательность:
        1) Создаем Recipe с title, time_type, cooking_time
        2) Создаем Специи, Этапы, Ингридиенты
            2.1) Высчитывать total_calories в RecipeIngredient
        3) Добавляем их в Recipe
            3.1) Высчитать total_calories, total_weight, all_calories в Recipe
    """
    if not data.get("ingredient_1"):
        return {"success": False, "message": "Нет ингредиентов"}
    if not data.get("title_stage_1"):
        return {"success": False, "message": "Нет этапов"}

    # Разъименум данные, они с формы приходят в списках
    data = renaming_kwargs_from_list(**data)

    # Создаем Recipe без relationships
    recipe = Recipe.objects.create(
        title=data["title"],
        time_type=data["time_type"],
        cooking_time=data["cooking_time"]
    )

    # Создаем PlaceSpices
    place_spices = create_objects_from_post(
        instance=recipe,
        object_to_create_name="place_spice",
        field="spice",
        **data
    )

    # Создаем CookStages
    cook_stages = create_objects_from_post(
        instance=recipe,
        object_to_create_name="cook_stage",
        field="title_stage",
        **data
    )

    # Создаем RecipeIngredients
    recipe_ingredients = create_objects_from_post(
        instance=recipe,
        object_to_create_name="recipe_ingredient",
        field="ingredient",
        **data
    )

    # Добавляем Созданные инстансы в Recipe
    recipe.spices.add(*place_spices)
    recipe.cook_stages.add(*cook_stages)
    recipe.recipe_ingredients.add(*recipe_ingredients)

    # Высчитываем каллорийность блюда, вес блюда, и общую каллорийность
    set_information_of_totals(recipe)
    return {"success": True, "message": recipe.title}


def create_cook(data):
    """
        1) Разъименовываем
        2) Создаем 'пустой' Cook с указанием рецепта
        3) Проверяем, установлен ли флаг is_change_count_ingredient
            3.1) Если установлен, то ингредиентам даем значения пользвотеля
            3.2) Если не установлен, то ингредиентам даем значения из рецепта
        4) Создаем CookIngredients
        ---) высчитываем total_calories для ингредиентов
        5) Высчитываем для Cook total_calories, total_weight, all_calories
        6) Сохраняем
    """

    # Разъименовываем данные из списков
    data = renaming_kwargs_from_list(**data)

    # Создаем пустой Cook
    cook = Cook.objects.create(recipe_id=data["recipe"])
    recipe = cook.recipe

    # Проверка флага is_change_count_ingredient
    if not data.get("is_change_count_ingredient"):
        # Замена в данных
        _set_in_data_like_post(recipe, data)

    # Создаем CookIngredients
    cook_ingredients = create_objects_from_post(
        instance=cook,
        object_to_create_name="cook_ingredient",
        field="ingredient",
        **data
    )

    # Вычитаем из склада использованные ингредиенты
    subtraction_from_store(*cook_ingredients)

    # Добавляем в Cook инстансы ингредиентов
    cook.cook_ingredients.add(*cook_ingredients)

    # Высчитываем для Cook total_calories, total_weight, all_calories
    set_information_of_totals(cook)

    return {"success": True, "message": recipe.title}


def _set_in_data_like_post(recipe: Recipe, data: dict) -> list:
    """Эта функция задает key value для работы метода create_cook"""
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    for i, recipe_ingredient in enumerate(recipe_ingredients):
        data["ingredient_" + str(i+1)] = recipe_ingredient.ingredient_id
        data['ingredient_count_use_' + str(i+1)] = recipe_ingredient.count_use
