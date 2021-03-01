from typing import Type

from django.db.models import Model


def set_model_in_context(instance: Type[Model], context: dict, *args, name_field=None):
    name_field = name_field or instance.__name__.lower() + "s"
    queryset = instance.objects.all()
    if len(args):
        queryset = queryset.values(*args)
    context[name_field] = queryset

