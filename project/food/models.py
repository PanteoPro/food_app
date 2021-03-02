from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

from .service.other import _isint

"""
Структура моделей приложения food
1) Spice - Специи
    1.1) PlaceSpice - Специи с указанием количества
2) CookStage - Этапы готовки
3) Ingredient - Ингредиент, категория
    3.1) IngredientItem - Хранилище, склад ингредиентов, указываются конкретные ингреедиенты из жизни
    3.2) RecipeIngredient - Ингредиент, который указывается в рецепте(не влияет на количество ингредиентов на складе)
    3.3) CookIngredient - Ингредиент, который указывается в блюде(влияет на количество ингредиентов на складе)
4) Recipe - Рецепт
5) Cook - Блюдо
6) Debt - Долг, если при готовке в базе не хватает наличия ингредиента
"""


class Spice(models.Model):
    """Специи"""
    title = models.CharField("Название", max_length=256)
    count_type = models.PositiveSmallIntegerField("В чем измеряется", choices=settings.TYPES_OF_COUNT_SPICES)

    def __str__(self):
        return "{} {}".format(self.title, settings.TYPES_OF_COUNT_SPICES[self.count_type-1][1])

    class Meta:
        verbose_name = "Специя"
        verbose_name_plural = "Специи"


class PlaceSpice(models.Model):
    """Специи с указанием количества"""
    spice = models.ForeignKey(Spice, verbose_name="Основа", on_delete=models.CASCADE)
    recipe = models.ForeignKey(to="Recipe", verbose_name="Блюдо", on_delete=models.CASCADE,
                               related_name="relates_spices")
    count_use = models.FloatField("Сколько используется в блюде",
                                  validators=[MinValueValidator(0.9), MaxValueValidator(58)])

    def format_count_use(self):
        if self.count_use == 0.25:
            return "1/4"
        if self.count_use == 0.5:
            return "1/2"
        if self.count_use == 0.75:
            return "3/4"

        if _isint(self.count_use):
            return int(self.count_use)
        return self.count_use

    def __str__(self):
        return "{} {}".format(self.spice.__str__(), self.count_use)

    class Meta:
        verbose_name = "Специя в рецепте"
        verbose_name_plural = "Специи в рецепте"


class CookStage(models.Model):
    """Стадии готовки"""
    title = models.CharField("Название этапа", max_length=256)
    recipe = models.ForeignKey(to="Recipe", verbose_name="Блюдо", on_delete=models.CASCADE,
                               related_name="relates_cook_stage")
    content = models.TextField("Описание этапа")
    time = models.PositiveSmallIntegerField("Длительность этапа")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Стадия готовки"
        verbose_name_plural = "Стадии готовки"


class Ingredient(models.Model):
    """Ингредиент (категория, класс, общее название), так как может быть несколько упаковок"""
    title = models.CharField("Название", max_length=256)
    count_type = models.PositiveSmallIntegerField("В чем измеряется", choices=settings.TYPES_OF_COUNT_INGREDIENTS)
    calories = models.PositiveSmallIntegerField("Калории на 100г продукта")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Ингредиенты"
        verbose_name_plural = "Ингредиенты"


class IngredientItem(models.Model):
    """Фактический ингредиент, ресурс"""
    ingredient = models.ForeignKey(Ingredient, verbose_name="Основа", on_delete=models.CASCADE,
                                   related_name="related_ingredient_items")
    count_start = models.PositiveSmallIntegerField("Начальное количество")
    count_now = models.PositiveSmallIntegerField("Текущее количество", blank=True)  # Заполнить в форме добавление автоматически
    manufacturer = models.CharField("Производитель", max_length=256)
    shelf_life = models.DateField("Конец срока годности")
    is_overdue = models.BooleanField("Просрочено?", default=False)
    is_ended = models.BooleanField("Закончилось?", default=False)

    def __str__(self):
        return f"Фактический ингредиент {self.ingredient.title} {self.manufacturer} " \
               f"{self.count_now}/{self.count_start} {settings.TYPES_OF_COUNT_INGREDIENTS[self.ingredient.count_type-1][1]}"

    class Meta:
        verbose_name = "Ингредиент на складе"
        verbose_name_plural = "Ингредиенты на складе"


class RecipeIngredient(models.Model):
    """
        Ингредиент, который указывается в Рецепте, нужен для указания количества
        Никак не влияет на количество продукта в наличии, так как привязан к классу(Ingredient)
    """
    ingredient = models.ForeignKey(Ingredient, verbose_name="Категория ингредиента", on_delete=models.CASCADE)
    recipe = models.ForeignKey(to="Recipe", verbose_name="Блюдо", on_delete=models.CASCADE,
                               related_name="relates_ingredient")
    count_use = models.PositiveSmallIntegerField("Сколько используется в блюде")
    total_calories = models.PositiveSmallIntegerField("Калории", blank=True, default=0)

    def __str__(self):
        return f"Ингредиент {self.ingredient.title} в рецепте {self.recipe}, {self.count_use} " \
               f"{settings.TYPES_OF_COUNT_INGREDIENTS[self.ingredient.count_type-1][1]}"

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"


class CookIngredient(models.Model):
    """
    Фактическая трата ингредиента
    Создаются при следующих ситуациях:
    1) Из рецепта, если в Cook флаг is_change_count_ingredient = False
    2) Вручную, в зависимости от введенных данных
    """
    ingredient_item = models.ForeignKey(
        to='IngredientItem',
        verbose_name="Основа",
        on_delete=models.CASCADE
    )
    cook = models.ForeignKey(
        to="Cook",
        verbose_name="Готовка",
        on_delete=models.CASCADE,
        related_name="relates_ingredient"
    )
    count_use = models.PositiveSmallIntegerField("Сколько используется в блюде", default=0)
    total_calories = models.PositiveSmallIntegerField("Калории", blank=True, default=0)

    def __str__(self):
        return f"Ингредиент в блюде {self.ingredient_item.ingredient.title}, " \
               f"{self.count_use} " \
               f"{settings.TYPES_OF_COUNT_INGREDIENTS[self.ingredient_item.ingredient.count_type-1][1]}"

    class Meta:
        verbose_name = "Ингредиент в блюде"
        verbose_name_plural = "Ингредиенты в блюде"


class Recipe(models.Model):
    """
    Рецепт, при создании блюда, создаются:
    0) Создается блюдо, с указанием: title, cooking_time, time_type
    1) Этапы готовки CookStage
    2) Ингредиенты RecipeIngredient
    3) Специи PlaceSpice
    4) Сохраняется
    """
    cook_stages = models.ManyToManyField(
        CookStage, verbose_name="Этапы готовки", related_name="related_recipe", blank=True
    )
    recipe_ingredients = models.ManyToManyField(
        RecipeIngredient, verbose_name="Ингредиенты", related_name="related_recipe", blank=True
    )
    spices = models.ManyToManyField(
        PlaceSpice, verbose_name="Специи", related_name="related_recipe", blank=True
    )
    title = models.CharField("Название", max_length=256)
    time_type = models.PositiveSmallIntegerField("Когда употребляется блюдо", choices=settings.TIME_TYPE_TO_USE)
    cooking_time = models.PositiveSmallIntegerField("Длительность готовки")
    total_weight = models.PositiveSmallIntegerField("Вес приготовленного блюда", blank=True, default=0)
    now_weight = models.PositiveSmallIntegerField("Сколько осталось блюда", blank=True, default=0)
    total_calories = models.PositiveSmallIntegerField("Калории на 100г продукта", blank=True, default=0)
    all_calories = models.PositiveSmallIntegerField("Общая каллорийность блюда", blank=True, default=0)

    def __str__(self):
        return self.title

    @property
    def cooking_time_format(self):
        return '{} мин'.format(self.cooking_time)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class Cook(models.Model):
    """Приготовленное блюдо"""
    recipe = models.ForeignKey(Recipe, verbose_name="Рецепт", on_delete=models.CASCADE)
    is_change_count_ingredient = models.BooleanField("Количество в приготовлении отличается от рецепта?", default=False)
    cook_ingredients = models.ManyToManyField(
        to=CookIngredient,
        verbose_name="Ингредиенты",
        related_name="related_cook",
        blank=True
    )
    total_weight = models.PositiveSmallIntegerField("Вес приготовленного блюда", blank=True, default=0)
    total_calories = models.PositiveSmallIntegerField("Калории", blank=True, default=0)
    all_calories = models.PositiveSmallIntegerField("Общая каллорийность блюда", blank=True, default=0)

    def __str__(self):
        return f"Блюдо {self.recipe.title}"

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"


class Debt(models.Model):
    ingredient = models.ForeignKey(Ingredient, verbose_name="Чего не хватает", on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField("Сколько не хватает")
    is_paid_of = models.BooleanField("Погасили долг", default=False)

    def __str__(self):
        return "{} {}".format(self.ingredient, self.count)

    class Meta:
        verbose_name = "Долг по складу"
        verbose_name_plural = "Долги по складу"
