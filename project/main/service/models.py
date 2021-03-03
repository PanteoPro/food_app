from typing import Union

from django.contrib.auth.models import User
from django.db.models import Q, QuerySet

from .other import get_start_today, get_end_today
from ..models import EatCook, Profile, EatIngredient

from food.models import Cook, IngredientItem


# ------------ Creates ------------ #

# ___ Profile ___ #


def create_model_profile(user: User, avatar=None, calories_limit=None, calories_now=None):
    """Создает профиль"""
    data = {"user": user}
    if avatar:
        data['avatar'] = avatar
    if calories_limit:
        data['calories_limit'] = calories_limit
    if calories_now:
        data['calories_now'] = calories_now
    return Profile.objects.create(**data)


# ___ EatCook ___ #


# ___ EatIngredient and EatCook ___ #

def create_model_eat(instance: Union[Cook, IngredientItem], profile: Profile, count_eat: int,
                     calories_eat=None, date=None):
    """Создает EatIngredient или EatCook"""
    class_name = instance.__class__.__name__
    data = {"profile": profile, "count_eat": count_eat}
    if calories_eat:
        data['calories_eat'] = calories_eat
    if date:
        data["date"] = date
    print(data)
    if class_name == "Cook":
        data["cook"] = instance
        return EatCook.objects.create(**data)
    elif class_name == "IngredientItem":
        data["ingredient_item"] = instance
        return EatIngredient.objects.create(**data)


# ------------ Gets ------------ #

# ___ Profile ___ #

def get_profile_by__user(user: User) -> Profile:
    """Возвращает инстанс профиля, по инстансу пользователя"""
    return Profile.objects.get(user=user)


# ___ EatCook ___ #

def get_eat_cook__today(profile: Profile, sort=False) -> QuerySet:
    """Возвращает QuerySet инстансов модели EatCook на сегодняшний день"""
    filter_set = (
            Q(profile=profile) &
            (Q(date__gte=get_start_today()) & Q(date__lte=get_end_today()))
    )
    if sort:
        return EatCook.objects.filter(filter_set).order_by("-id")
    return EatCook.objects.filter(filter_set)


def get_eat_cook__already(profile: Profile) -> QuerySet:
    """Возвращает все EatCook, которые можно съесть"""

# ___ EatIngredient ___ #


def get_eat_ingredient__today(profile: Profile, sort=False) -> QuerySet:
    """Возвращает QuerySet инстансов модели EatIngredient на сегодняшний день"""
    filter_set = (
            Q(profile=profile) &
            (Q(date__gte=get_start_today()) & Q(date__lte=get_end_today()))
    )
    if sort:
        return EatIngredient.objects.filter(filter_set).order_by("-id")
    return EatIngredient.objects.filter(filter_set)
