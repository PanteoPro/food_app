# Generated by Django 3.1.7 on 2021-02-26 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_change_count_ingredient', models.BooleanField(default=False, verbose_name='Количество в приготовлении отличается от рецепта?')),
                ('total_weight', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Вес приготовленного блюда')),
                ('total_calories', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Калории')),
            ],
        ),
        migrations.CreateModel(
            name='CookStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название этапа')),
                ('content', models.TextField(verbose_name='Описание этапа')),
                ('time', models.PositiveSmallIntegerField(verbose_name='Длительность этапа')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('count_type', models.PositiveSmallIntegerField(choices=[(1, 'грамм'), (2, 'шт'), (3, 'мл')], verbose_name='В чем измеряется')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_start', models.PositiveSmallIntegerField(verbose_name='Начальное количество')),
                ('count_now', models.PositiveSmallIntegerField(verbose_name='Текущее количество')),
                ('manufacturer', models.CharField(max_length=256, verbose_name='Производитель')),
                ('shelf_life', models.DateField(verbose_name='Конец срока годности')),
                ('calories', models.PositiveSmallIntegerField(verbose_name='Калории на 100г продукта')),
                ('is_overdue', models.BooleanField(default=False, verbose_name='Просрочено?')),
                ('is_ended', models.BooleanField(default=False, verbose_name='Закончилось?')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.ingredient', verbose_name='Основа')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceSpice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_use', models.PositiveSmallIntegerField(verbose_name='Сколько используется в блюде')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('time_type', models.PositiveSmallIntegerField(choices=[(1, 'завтрак'), (2, 'обед'), (3, 'ужин'), (4, 'перекус')], verbose_name='Когда употребляется блюдо')),
                ('cooking_time', models.PositiveSmallIntegerField(verbose_name='Длительность готовки')),
                ('total_calories', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Калории на 100г продукта')),
                ('cook_stages', models.ManyToManyField(blank=True, related_name='related_recipe', to='food.CookStage', verbose_name='Этапы готовки')),
            ],
        ),
        migrations.CreateModel(
            name='Spice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('count_type', models.PositiveSmallIntegerField(choices=[(1, 'шепотка'), (2, 'чайная ложка'), (3, 'столовая ложка')], verbose_name='В чем измеряется')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_use', models.PositiveSmallIntegerField(verbose_name='Сколько используется в блюде')),
                ('total_calories', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Калории')),
                ('ingredient_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.ingredientitem', verbose_name='Основа')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relates_ingredient', to='food.recipe', verbose_name='Блюдо')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_ingredients',
            field=models.ManyToManyField(blank=True, related_name='related_recipe', to='food.RecipeIngredient', verbose_name='Ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='spices',
            field=models.ManyToManyField(blank=True, related_name='related_recipe', to='food.PlaceSpice', verbose_name='Специи'),
        ),
        migrations.AddField(
            model_name='placespice',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relates_spices', to='food.recipe', verbose_name='Блюдо'),
        ),
        migrations.AddField(
            model_name='placespice',
            name='spice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.spice', verbose_name='Основа'),
        ),
        migrations.AddField(
            model_name='cookstage',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relates_cook_stage', to='food.recipe', verbose_name='Блюдо'),
        ),
        migrations.CreateModel(
            name='CookIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_use', models.PositiveSmallIntegerField(verbose_name='Сколько используется в блюде')),
                ('total_calories', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Калории')),
                ('cook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relates_ingredient', to='food.cook', verbose_name='Готовка')),
                ('ingredient_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.ingredientitem', verbose_name='Основа')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='cook',
            name='cook_ingredient',
            field=models.ManyToManyField(blank=True, related_name='related_cook', to='food.CookIngredient', verbose_name='Ингредиенты'),
        ),
        migrations.AddField(
            model_name='cook',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.recipe', verbose_name='Рецепт'),
        ),
    ]
