from typing import Union

from .models import get_model_ingredient_item_by__ingredient_id__already, create_debt
from ..models import CookIngredient, IngredientItem, Debt, Recipe, Cook, Ingredient


# ____________ Checks ------------ #

# ___ Ingredient_Item ___ #

def check_ingredient_for_end(ingredient_item: IngredientItem, count_use: int) -> bool:
    """Если мы из IngredientItem вычтем количество в count_use, останется ли положительное число?"""
    result_count = int(ingredient_item.count_now - count_use)
    if result_count > 0:
        return False
    return True


# ___ Debt ___ #

def check_debt_for_ingredient_item(ingredient_item: IngredientItem) -> dict:
    """Проверяет есть ли долги до данному ингредиенту, и если есть за оплатить по долгам"""
    ingredient = ingredient_item.ingredient
    debts = Debt.objects.filter(ingredient=ingredient, is_paid_of=False)
    count_start = count_now = ingredient_item.count_now

    is_all_redeemed = True
    messages = list()

    if len(debts):
        for debt in debts:
            count_debt = debt.count
            count_now -= count_debt
            if count_now <= 0:
                is_all_redeemed = False
                messages.append("Ингредиент добавлен, но полностью был использован для погашения долгов")
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
            messages.append("Ингредиент добавлен. Все долги погашены, осталось {} из {}".format(count_now, count_start))
    else:
        messages.append("Ингредиент добавлен")

    if is_all_redeemed:
        ingredient_item.count_now = count_now
        ingredient_item.save()

    return {"success": is_all_redeemed, "messages": messages}


# __ IngredientItem ___ #

def check_ingredient_item__count(**data) -> dict: # Надо ее переписать
    """Проверка, хвататет ли ингредиентов на складе, чтобы создать Cook"""
    success = True
    messages = list()
    number = 1
    while True:
        if not data.get("ingredient_" + str(number)):
            break

        count_use = data['ingredient_count_use_' + str(number)]

        ingredient_id = data['ingredient_' + str(number)]
        ingredient_title = Ingredient.objects.get(pk=ingredient_id)
        ingredient_items = IngredientItem.objects.filter(ingredient_id=ingredient_id,
                                                         is_ended=False, is_overdue=False)

        if len(ingredient_items) == 0:
            messages.append("Нет в наличии ингредиента {}".format(ingredient_title))
            success = False
        else:
            sum_count_have = 0
            for ingredient_item in ingredient_items:
                sum_count_have += ingredient_item.count_now
            if sum_count_have < count_use:
                messages.append(f"Нехватает ингредиента {ingredient_title}. "
                                f"Нужно {count_use}, на складе есть {sum_count_have}")
                success = False
        number += 1

    return {"success": success, "messages": messages}

# ____________ Changes ------------ #


# ___ Ingredient_Item ___ #

def change_ingredient_item_from__cook_ingredients(*cook_ingredients: CookIngredient) -> None:
    """
        Можно передать один или несколько CookIngredients
        Вычитаем из базы данных, количество текущего ингридиента
        Если в привязяанном ingredient_item, будет недостаточное количество:
            1) is_ended поставит true
            2) Метод попробует вычесть из других под этим же классом
        Если на складе будет недостаточно ингредиентов, создастся долг
    """
    for cook_ingredient in cook_ingredients:
        ingredient_item = cook_ingredient.ingredient_item
        count_to_subtract = cook_ingredient.count_use
        result = change_ingredient_item__count_now(ingredient_item, count_to_subtract)
        if result:
            debt = True
            already_ingredients = get_model_ingredient_item_by__ingredient_id__already(ingredient_item)
            if len(already_ingredients):
                for ingredient in already_ingredients:
                    result = change_ingredient_item__count_now(ingredient, result)
                    if not result:
                        debt = False
                        break

            if debt:
                create_debt(ingredient_item, result)
                print("Остался долг {}! Добавляем его".format(result))


def change_ingredient_item__count_now(ingredient_item: IngredientItem, count_use=0) -> int:
    """
        Меняет у IngredientItem текущее значение в наличии:
         - на 0,если не хватает и возвращает непокрытый долг
         - иначе просто вычтет значение
    """
    if check_ingredient_for_end(ingredient_item, count_use):
        result_count = abs(int(ingredient_item.count_now - count_use))
        ingredient_item.count_now = 0
        ingredient_item.is_ended = True
        ingredient_item.save()
        return result_count
    else:
        ingredient_item.count_now = int(ingredient_item.count_now) - int(count_use)
        ingredient_item.save()
        return 0


# ___ Recipe and Cook ___ #

def change_cook_recipe_totals(instance: Union[Recipe, Cook]) -> None:
    """Добавляется в instance Recipe или Cook
    значения полей total_calories, total_weight, all_calories и now_weight для Cook"""
    ingredients = None
    choice = None
    if instance.__class__.__name__ == "Recipe":
        ingredients = instance.recipe_ingredients.all()
        choice = "recipe"
    elif instance.__class__.__name__ == "Cook":
        ingredients = instance.cook_ingredients.all()
        choice = "cook"
    information = count_cook_recipe_totals(ingredients, weight=True, all_calories=True)
    instance.total_calories = information['total_calories']
    instance.total_weight = information['total_weight']
    if choice == "cook":
        instance.now_weight = information['total_weight']
    instance.all_calories = information['all_calories']
    instance.save()


# ___ Cook ___ #

def change_cook__now_weight(cook: Cook, count: int):
    """Уменьшает количество блюда на count"""
    cook.now_weight -= count
    if cook.now_weight == 0:
        cook.is_ended = True
    cook.save()

# ____________ Counts ------------ #


# ___ Recipe and Cook ___ #

def count_cook_recipe_totals(ingredients, weight=False, all_calories=False):
    """
        Из queryset'a CookIngredient или RecipeIngredient считается:
         1) конечное количество каллорий на 100 грамм
         2) конечный вес блюда, если передан флаг weight
         3) конечное количество калорий блюда, если передан флаг all_calories
        Возвращается dict, total_calories, total_weight, all_calories
    """
    total_calories = calories_sum = weight_sum = 0
    result = dict()
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
                result["total_weight"] = weight_sum
            if all_calories:
                result["all_calories"] = calories_sum
            result["total_calories"] = total_calories
            return result
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

