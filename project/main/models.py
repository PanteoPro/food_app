from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from .service.other import get_path_for_avatar


class Profile(models.Model):
    """Профиль"""

    user = models.OneToOneField(User, verbose_name="Объект пользователя", on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name="Аватарка", upload_to=get_path_for_avatar, blank=True)
    calories_limit = models.PositiveSmallIntegerField("Лимит калорий в день", default=0, blank=True)
    calories_now = models.PositiveSmallIntegerField("Сколько употреблено на сегодня", default=0, blank=True)

    def get_avatar(self):
        """Возвращает ссылку на аватарку, если она не указана, вернется анонимный аватар"""
        if not self.avatar:
            return settings.ANONYMOUS_AVATAR_URL
        return self.avatar.url

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Eating(models.Model):

    class Meta:
        abstract = True

    date = models.DateTimeField("Когда употреблено", default=datetime.now)
    count_eat = models.PositiveSmallIntegerField("Сколько грамм употреблено")
    calories_eat = models.PositiveSmallIntegerField("Сколько калорий употреблено", default=0, blank=True)


class EatCook(Eating):
    """Употребляемое блюдо"""

    cook = models.ForeignKey("food.Cook", verbose_name="Блюдо", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, verbose_name="Профиль", on_delete=models.CASCADE,
                                related_name="related_eat_cooks")

    def __str__(self):
        return f"{self.cook.recipe.title} - {self.profile.user.username}"

    class Meta:
        verbose_name = "Употребленное блюдо"
        verbose_name_plural = "Употребленное блюда"


class EatIngredient(Eating):
    """Употребляемый ингредиент"""

    ingredient_item = models.ForeignKey("food.IngredientItem", verbose_name="Продукт", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, verbose_name="Профиль", on_delete=models.CASCADE,
                                related_name="related_eat_ingredient")

    def __str__(self):
        return f"Употребление продукта {self.ingredient_item.ingredient.title}"

    class Meta:
        verbose_name = "Употребленный продукт"
        verbose_name_plural = "Употребленные продукты"

