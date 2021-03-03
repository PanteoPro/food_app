from ..models import Recipe, Cook
from .essential import change_cook_recipe_totals, \
    check_ingredient_item__count, change_ingredient_item_from__cook_ingredients, check_debt_for_ingredient_item
from .post_manager import renaming_kwargs_from_list, create_objects_from_post, \
    _set_in_data_like_post


def create_ingredient_item(form):
    """
        Создает в базе запись IngredientItem из данных формы
        Перед сохранением проверяет есть ли долги по ингредиенту
    """
    ingredient_item = form.save(commit=False)
    result = check_debt_for_ingredient_item(ingredient_item)
    return result


def create_recipe(data):
    """
        Последовательность:
        1) Создаем Recipe с title, time_type, cooking_time
        2) Создаем Специи, Этапы, Ингридиенты
            2.1) Высчитывать total_calories в RecipeIngredient
        3) Добавляем их в Recipe
            3.1) Высчитать total_calories, total_weight, all_calories в Recipe
    """
    messages = []
    success = True
    if not data.get("ingredient_1"):
        messages.append("Нет ингредиентов")
        success = False
    if not data.get("title_stage_1"):
        messages.append("Нет этапов")
        success = False
    if not success:
        return {"success": success, 'messages': messages}

    # Разъименум данные, они с формы приходят в списках
    data = renaming_kwargs_from_list(**data)

    # Создаем Recipe без relationships
    recipe = Recipe.objects.create(
        title=data["title"],
        time_type=data["time_type"],
        cooking_time=data["cooking_time"],
        days_to_overdue=data["days_to_overdue"]
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
    change_cook_recipe_totals(recipe)
    return {"success": True, "messages": [recipe.title]}


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
    recipe = Recipe.objects.get(pk=data['recipe'])

    # Проверка флага is_change_count_ingredient
    if not data.get("is_change_count_ingredient"):
        # Замена в данных
        _set_in_data_like_post(recipe, data)

    # Проверка на наличие ингредиентов
    result_checking = check_ingredient_item__count(**data)
    if not result_checking['success']:
        return result_checking

    # Создаем пустой Cook
    cook = Cook.objects.create(recipe=recipe)

    # Создаем CookIngredients
    cook_ingredients = create_objects_from_post(
        instance=cook,
        object_to_create_name="cook_ingredient",
        field="ingredient",
        **data
    )

    # Вычитаем из склада использованные ингредиенты
    change_ingredient_item_from__cook_ingredients(*cook_ingredients)

    # Добавляем в Cook инстансы ингредиентов
    cook.cook_ingredients.add(*cook_ingredients)

    # Высчитываем для Cook total_calories, total_weight, all_calories
    change_cook_recipe_totals(cook)

    return {"success": True, "messages": [recipe.title]}


