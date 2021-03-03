from typing import Type

from django.db.models import Model


def set_model_all_in_context(instance: Type[Model], context: dict, *args, name_field=None):
    """
    Вставляет в словарь context ключ name_field или название класса + 's'
    С данными из instance.all
    В *args передаются значения, которые хотим достать из Queryset
    """
    name_field = name_field or instance.__name__.lower() + "s"
    queryset = instance.objects.all()
    if len(args):
        queryset = queryset.values(*args)
    context[name_field] = queryset


def set_model_filter_in_context(instance: Type[Model], context: dict, *args, name_field=None, **kwargs):
    """
    Вставляет в словарь context ключ name_field или название класса + 's'
    С данными из instance.filter
    В *args передаются значения, которые хотим достать из Queryset
    В **kwargs передаются значения, которые фильтруют
    """
    name_field = name_field or instance.__name__.lower() + "s"
    filter_queryset = instance.objects.filter(**kwargs)
    if len(args):
        queryset = filter_queryset.values(*args)
    context[name_field] = filter_queryset


def set_model_get_in_context(instance: Type[Model], context: dict, name_field=None, **kwargs):
    """
        Вставляет в словарь context ключ name_field или название класса
        С данными из instance.get
        В **kwargs передаются значения, которые фильтруют
    """
    name_field = name_field or instance.__name__.lower()
    find_instance = instance.objects.get(**kwargs)
    context[name_field] = find_instance
