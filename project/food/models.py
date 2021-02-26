from django.db import models
from django.conf import settings


class TypeIngredient(models.Model):

    class Meta:
        abstract = True

    ingredient_item = models.ForeignKey(
        to='IngredientItem',
        verbose_name="Основа",
        on_delete=models.CASCADE
    )
    count_use = models.PositiveSmallIntegerField("Сколько используется в блюде")
    total_calories = models.PositiveSmallIntegerField("Калории", blank=True, default=0)

    def __str__(self):
        return "{} {} {}".format(
            self.ingredient_item.ingredient.title,
            self.count_use,
            self.ingredient_item.manufacturer
        )


class Spice(models.Model):
    """Специи"""
    title = models.CharField("Название", max_length=256)
    count_type = models.PositiveSmallIntegerField("В чем измеряется", choices=settings.TYPES_OF_COUNT_SPICES)

    def __str__(self):
        return "{} {}".format(self.title, settings.TYPES_OF_COUNT_SPICES[self.count_type-1][1])


class PlaceSpice(models.Model):
    """Специи с указанием количества"""
    spice = models.ForeignKey(Spice, verbose_name="Основа", on_delete=models.CASCADE)
    recipe = models.ForeignKey(to="Recipe", verbose_name="Блюдо", on_delete=models.CASCADE,
                               related_name="relates_spices")
    count_use = models.PositiveSmallIntegerField("Сколько используется в блюде")

    def __str__(self):
        return "{} {}".format(self.spice.__str__(), self.count_use)


class Ingredient(models.Model):
    """Ингредиент (категория, класс, общее название), так как может быть несколько упаковок"""
    title = models.CharField("Название", max_length=256)
    count_type = models.PositiveSmallIntegerField("В чем измеряется", choices=settings.TYPES_OF_COUNT_INGREDIENTS)

    def __str__(self):
        return self.title


class IngredientItem(models.Model):
    """Фактический ингредиент, ресурс"""
    ingredient = models.ForeignKey(Ingredient, verbose_name="Основа", on_delete=models.CASCADE)
    count_start = models.PositiveSmallIntegerField("Начальное количество")
    count_now = models.PositiveSmallIntegerField("Текущее количество")  # Заполнить в форме добавление автоматически
    manufacturer = models.CharField("Производитель", max_length=256)
    shelf_life = models.DateField("Конец срока годности")
    calories = models.PositiveSmallIntegerField("Калории на 100г продукта")
    is_overdue = models.BooleanField("Просрочено?", default=False)
    is_ended = models.BooleanField("Закончилось?", default=False)

    def __str__(self):
        return self.ingredient.title


class RecipeIngredient(TypeIngredient):
    """Ингредиент, который указывается в Рецепте, нужен для указания количества"""
    recipe = models.ForeignKey(to="Recipe", verbose_name="Блюдо", on_delete=models.CASCADE,
                               related_name="relates_ingredient")


class CookStage(models.Model):
    """Стадии готовки"""
    title = models.CharField("Название этапа", max_length=256)
    recipe = models.ForeignKey(to="Recipe", verbose_name="Блюдо", on_delete=models.CASCADE,
                               related_name="relates_cook_stage")
    content = models.TextField("Описание этапа")
    time = models.PositiveSmallIntegerField("Длительность этапа")

    def __str__(self):
        return self.title


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
    total_calories = models.PositiveSmallIntegerField("Калории на 100г продукта", blank=True, default=0)

    def __str__(self):
        return self.title

    @property
    def cooking_time_format(self):
        return '{} мин'.format(self.cooking_time)


class CookIngredient(TypeIngredient):
    """
    Фактическая трата ингредиента
    Создаются при следующих ситуациях:
    1) Из рецепта, если в Cook флаг is_change_count_ingredient = False
    2) Вручную, в зависимости от введенных данных
    """
    cook = models.ForeignKey(to="Cook", verbose_name="Готовка", on_delete=models.CASCADE,
                             related_name="relates_ingredient")

    def save(self, *args, **kwargs):
        from .service.admin import change_count_from_ingredient_item
        change_count_from_ingredient_item(self)
        super().save(*args, **kwargs)


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

    def __str__(self):
        return self.recipe.title


class Debt(models.Model):
    ingredient = models.ForeignKey(Ingredient, verbose_name="Чего не хватает", on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField("Сколько не хватает")
    is_paid_of = models.BooleanField("Погасили долг", default=False)

    def __str__(self):
        return "{} {}".format(self.ingredient, self.count)
