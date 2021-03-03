def _isint(value):
    """Проверка значение на тип int"""
    try:
        int(value)
        return True
    except ValueError:
        return False


def _isfloat(value):
    """Проверка значение на тип float"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_total_calories_for_ingredient(calories: int, count_use: int) -> int:
    """Эта функция высчитывает количество каллорий в ингредиенте"""
    if calories and count_use:
        return int(calories * (count_use/100))