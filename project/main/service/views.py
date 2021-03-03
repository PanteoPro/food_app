from datetime import datetime

from django.contrib import messages as django_messages

from .essential import add_model_profile_to__calories_now, check_have_username
from .models import (
    get_eat_cook__today,
    get_profile_by__user,
    create_model_eat
)
from food.service.models import get_model_cook_by__id, get_model_ingredient_item_by__id
from food.service.essential import change_cook__now_weight, change_ingredient_item__count_now


def set_info_for_profile_in_context(context, user):
    """"""
    profile = get_profile_by__user(user)
    eat_cooks = get_eat_cook__today(profile)
    # print(eat_cooks)


def message_manager(request, result: dict) -> None:
    """Отрпавляет пришедшие сообщение на сайт"""
    message_tag = django_messages.INFO
    if not result['success']:
        message_tag = django_messages.ERROR
    for message in result['messages']:
        django_messages.add_message(request, message_tag, message)


def change_profile(request: dict) -> dict:
    """
        Применяет настройки профиля
        - Изменяет аватарку
        - Изменяет ник
        - Изменяет лимит калорий в день
        Возвращает результат применения настроек с сообщениями
    """
    success = True
    messages = []

    # Начальные данные
    data = request.POST
    files = request.FILES
    user = request.user
    profile = get_profile_by__user(user)

    avatar = files.get("avatar")
    username = data.get("username")
    calories_limit = data.get("calories_limit")

    # Если передали аватар
    if avatar:
        ext = avatar.name.split(".")[1]
        if ext == "jpg" or ext == "png":
            profile.avatar = avatar
        else:
            messages.append("Приложение не принимает картинки формата {}".format(ext))
            success = False

    # Если передали ник
    if username != user.username and success:
        if not check_have_username(username):
            messages.append(f"Изменили ник с {user.username} на {username}")
            user.username = username
        else:
            messages.append("Пользователь с таким ником существует")
            success = False

    # Если передали лимит калорий
    if calories_limit != profile.calories_limit and success:
        messages.append(f"Изменили лимит калорий с {profile.calories_limit} на {calories_limit}")
        profile.calories_limit = calories_limit

    # Сохраняем
    if success:
        user.save()
        profile.save()

    return {"success": success, "messages": messages}


def create_eat_cook(request: dict) -> dict:
    """
        Создает EatCook
        Возвращает результат создания с сообщениями
    """
    success = True
    messages = []

    # Начальные данные
    data = request.POST
    user = request.user
    profile = get_profile_by__user(user)
    cook = get_model_cook_by__id(data['cook'])

    date = data['date']
    count_eat = int(data['count_eat'])

    # Высчитываем сколько каллорий употреблено
    calories_eat = int((count_eat/100) * cook.total_calories)

    # Создаем EatCook
    if cook.now_weight >= count_eat:
        create_model_eat(cook, profile, count_eat, calories_eat, date=date)
    else:
        success = False
        messages.append("Вы ввели больше чем есть. Блюда осталось {} грамм".format(cook.now_weight))

    if success:
        # Меняем в профиле количество калорий на текущий день
        add_model_profile_to__calories_now(profile, calories_eat)

        # Меняем количество блюда
        change_cook__now_weight(cook, count_eat)

        messages.append(f"Добавили употребление блюда {cook} в размере {count_eat}г")
    return {"success": success, "messages": messages}


def create_eat_ingredient(request: dict) -> dict:
    """Создает EatIngredient
    Возвращает результат создания с сообщениями"""
    success = True
    messages = []

    # Начальные данные
    data = request.POST
    user = request.user
    profile = get_profile_by__user(user)
    ingredient_item = get_model_ingredient_item_by__id(data['ingredient_item'])

    date = data['date']
    count_eat = int(data['count_eat'])

    # Высчитываем сколько каллорий употреблено
    calories_eat = int((count_eat / 100) * ingredient_item.ingredient.calories)

    # Создаем EatCook
    if ingredient_item.count_now >= count_eat:
        create_model_eat(ingredient_item, profile, count_eat, calories_eat, date=date)
    else:
        success = False
        messages.append("Вы ввели больше чем есть. Ингредиента осталось {} грамм".format(ingredient_item.count_now))

    if success:
        # Меняем в профиле количество калорий на текущий день
        add_model_profile_to__calories_now(profile, calories_eat)

        # Меняем количество блюда
        change_ingredient_item__count_now(ingredient_item, count_eat)

        messages.append(f"Добавили употребление блюда {ingredient_item.ingredient.title} в размере {count_eat}г")
    return {"success": success, "messages": messages}
