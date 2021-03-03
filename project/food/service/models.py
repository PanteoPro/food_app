from django.db.models import QuerySet

from ..models import Cook, IngredientItem, Debt


# ____________ Creates ------------ #


# ___ Debt ___ #

def create_debt(ingredient_item: IngredientItem, count: int) -> Debt:
    """Создание долга"""
    return Debt.objects.create(ingredient=ingredient_item.ingredient, count=count)

# ____________ Gets ------------ #


# ___ Cook ___ #

def get_model_cook_by__id(id_cook) -> Cook:
    """Возвращает инстанс модели Cook по id
    Данные принимаются в любом из форматов python"""
    if isinstance(id_cook, (list, tuple)):
        id_cook = id_cook[0]
    elif isinstance(id, dict):
        id_cook = id_cook["id"]
    return Cook.objects.get(pk=id_cook)


def get_model_cook__already() -> QuerySet:
    """Возвращает все блюда которые есть в наличии и не просроченны"""
    return Cook.objects.filter(is_ended=False, is_overdue=False)

# ___ IngredientItem ___ #


def get_model_ingredient_item_by__id(id_ingredient_item) -> IngredientItem:
    """Возвращает инстанс модели IngredientItem по id"""
    if isinstance(id_ingredient_item, (list, tuple)):
        id_cook = id_ingredient_item[0]
    elif isinstance(id, dict):
        id_cook = id_ingredient_item["id"]
    return IngredientItem.objects.get(pk=id_ingredient_item)


def get_model_ingredient_item_by__ingredient_id__already(ingredient_item: IngredientItem) -> QuerySet:
    """Возвращает QuerySet объектов IngredientItem по ingredient
    которые еще не закончились и не просрочились"""
    return IngredientItem.objects.filter(ingredient=ingredient_item.ingredient, is_ended=False, is_overdue=False)


def get_model_ingredient_item__already() -> QuerySet:
    """Возвращает всее ингредиенты которые есть в наличии и не просроченны"""
    return IngredientItem.objects.filter(is_ended=False, is_overdue=False)

