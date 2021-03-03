from django.contrib.auth.models import User
from django.db.models import Sum

from .models import get_profile_by__user, get_eat_cook__today, get_eat_ingredient__today
from ..models import Profile


# ____________ Adds ------------ #

# ___ Profile ___ #


def add_model_profile_to__calories_now(profile: Profile, add_calories: int, commit=True) -> None:
    """Добавляет калории в профиле, Сохраняет"""
    profile.calories_now += add_calories
    if commit:
        profile.save()


def update_profile(user: User):
    """Обновление данных в профиле"""
    calories_now = 0
    profile = get_profile_by__user(user)
    eat_cooks = get_eat_cook__today(profile)
    eat_ingredients = get_eat_ingredient__today(profile)
    if eat_cooks.exists():
        calories_now += eat_cooks.aggregate(Sum("calories_eat"))['calories_eat__sum']
    if eat_ingredients.exists():
        calories_now += eat_ingredients.aggregate(Sum("calories_eat"))['calories_eat__sum']
    profile.calories_now = calories_now
    profile.save()

# ___ EatCook ___ #

# ____________ Checks ------------ #


def check_have_username(username):
    """Проверяет наличие ника в базе
    Возвращает true если нашел, false если нет"""
    if isinstance(list, tuple):
        username = username[0]
    if User.objects.filter(username=username).exists():
        return True
    return False

