from django.db.models import QuerySet


def get_total_calories_from_ingredients(ingredients: QuerySet) -> float:
    """Из queryset'a PlaceIngredient считается конечное количество каллорий на 100 грамм"""
    calories_sum = weight_sum = 0
    for item in ingredients:
        weight_sum += int(item.count_use)
        calories_sum += int(item.total_calories)
    total_calories = calories_sum / weight_sum * 100
    print(weight_sum, calories_sum)
    return total_calories


def get_total_calories_from_calories_and_count_calories(calories: int, count_gramms: int) -> int:
    return int(calories * (count_gramms/100))
