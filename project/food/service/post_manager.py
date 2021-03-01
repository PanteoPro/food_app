from .other import _isint, _isfloat
from ..models import Recipe, PlaceSpice, CookStage, RecipeIngredient, CookIngredient, Cook, Ingredient


def create_objects_from_post(instance, object_to_create_name, field, **kwargs) -> list:
    """
        Это фукнция вызывает функции, которые создают instance моделей, на основе данных из post
        Передавая в них данные из формы в kwargs
        Доступны модели для создания - PlaceSpice, CookStage, RecipeIngredient,CookIngredient
    """
    func = None
    if object_to_create_name == "place_spice":
        func = _create_place_spice
    elif object_to_create_name == "cook_stage":
        func = _create_cook_stage
    elif object_to_create_name == "recipe_ingredient":
        func = _create_recipe_ingredient
    elif object_to_create_name == "cook_ingredient":
        func = _create_cook_ingredient

    result_objects = []
    i = 1
    while True:
        if not kwargs.get(field + "_" + str(i)):
            break
        result_objects.append(func(instance, i, **kwargs))
        i += 1
    return result_objects


def _create_place_spice(recipe: Recipe, number: int, **kwargs) -> PlaceSpice:
    """Создает instance PlaceSpice из данных в kwargs.
    Работает только в контексте create_recipe"""
    spice_id = kwargs['spice_' + str(number)]
    count_use = kwargs['count_use_spice_' + str(number)]
    return PlaceSpice.objects.create(
        spice_id=spice_id,
        count_use=count_use,
        recipe=recipe
    )


def _create_cook_stage(recipe: Recipe, number: int, **kwargs) -> CookStage:
    """Создает instance CookStage из данных в kwargs.
    Работает только в контексте create_recipe"""
    title = kwargs['title_stage_' + str(number)]
    content = kwargs['content_stage_' + str(number)]
    time_stage = kwargs['time_stage_' + str(number)]
    return CookStage.objects.create(
        title=title,
        content=content,
        time=time_stage,
        recipe=recipe
    )


def _create_recipe_ingredient(recipe: Recipe, number: int, **kwargs) -> RecipeIngredient:
    """Создает instance CookStage из данных в kwargs. Так же высчитывает каллории, основываясь на instance Ingredient
    Работает только в контексте create_recipe"""
    ingredient_id = kwargs['ingredient_' + str(number)]
    count_use = kwargs['count_use_ingredient_' + str(number)]

    calories = Ingredient.objects.get(pk=ingredient_id).calories

    total_calories = int(_get_total_calories_for_ingredient(calories, count_use))
    return RecipeIngredient.objects.create(
        ingredient_id=ingredient_id,
        count_use=count_use,
        total_calories=total_calories,
        recipe=recipe
    )


def _create_cook_ingredient(cook: Cook, number: int, **kwargs) -> CookIngredient:
    """Создает instance CookIngredient из данных в kwargs.
        Работает только в контексте create_recipe"""
    ingredient_id = kwargs['ingredient_' + str(number)]
    count_use = kwargs['ingredient_count_use_' + str(number)]

    ingredient = Ingredient.objects.get(pk=ingredient_id)
    ingredient_item = ingredient.related_ingredient_items.first()
    calories = ingredient.calories

    total_calories = _get_total_calories_for_ingredient(calories, count_use)

    return CookIngredient.objects.create(
        ingredient_item=ingredient_item,
        count_use=count_use,
        total_calories=total_calories,
        cook=cook
    )


def renaming_kwargs_from_list(**kwargs):
    """Разъименовывает данные, если они в массивах, так же приводит к нужному типу"""
    wrapper = None
    for field_name in kwargs:
        value = kwargs[field_name]
        value_choice_wrapper = value[0]
        if _isint(value_choice_wrapper):
            wrapper = int
        elif _isfloat(value_choice_wrapper):
            wrapper = float
        else:
            wrapper = str
        kwargs[field_name] = wrapper(*value)
    return kwargs


def _get_total_calories_for_ingredient(calories: int, count_use: int) -> int:
    """Эта функция высчитывает количество каллорий в ингредиенте"""
    if calories and count_use:
        return int(calories * (count_use/100))