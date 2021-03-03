from django import template

from ..models import Profile
from ..service.models import get_eat_cook__today, get_eat_ingredient__today

register = template.Library()


def get_eat_cooks(profile):
    eat_cooks = get_eat_cook__today(profile, sort=True)
    return {"eat_cooks": eat_cooks}


def get_eat_ingredients(profile):
    ingredient_items = get_eat_ingredient__today(profile, sort=True)
    return {"eat_ingredient_items": ingredient_items}


@register.inclusion_tag("tags/now_eating.html")
def get_eats(user):
    profile = Profile.objects.get(user=user)
    data = get_eat_cooks(profile)
    data.update(get_eat_ingredients(profile))
    return data
