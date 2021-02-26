# Generated by Django 3.1.7 on 2021-02-26 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('time_type', models.PositiveSmallIntegerField(choices=[(1, 'завтрак'), (2, 'обед'), (3, 'ужин'), (4, 'перекус')], verbose_name='Когда употребляется блюдо')),
                ('cooking_time', models.PositiveSmallIntegerField(verbose_name='Длительность готовки')),
                ('total_calories', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Калории на 100г продукта')),
                ('cook_stages', models.ManyToManyField(blank=True, related_name='related_food', to='food.CookStage', verbose_name='Этапы готовки')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_type', models.PositiveSmallIntegerField(choices=[(1, 'грамм'), (2, 'шт'), (3, 'мл')], verbose_name='В чем измеряется')),
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
            name='Spice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Название')),
                ('count_type', models.PositiveSmallIntegerField(choices=[(1, 'шепотка'), (2, 'чайная ложка'), (3, 'столовая ложка')], verbose_name='В чем измеряется')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceSpice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_use', models.PositiveSmallIntegerField(verbose_name='Сколько используется в блюде')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relates_spices', to='food.food', verbose_name='Блюдо')),
                ('spice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.spice', verbose_name='Основа')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_use', models.PositiveSmallIntegerField(verbose_name='Сколько используется в блюде')),
                ('total_calories', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Калории')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relates_ingredient', to='food.food', verbose_name='Блюдо')),
                ('ingredient_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.ingredientitem', verbose_name='Основа')),
            ],
        ),
        migrations.AddField(
            model_name='food',
            name='ingredient_items',
            field=models.ManyToManyField(blank=True, related_name='related_food', to='food.PlaceIngredient', verbose_name='Ингредиенты'),
        ),
        migrations.AddField(
            model_name='food',
            name='spices',
            field=models.ManyToManyField(blank=True, related_name='related_food', to='food.PlaceSpice', verbose_name='Специи'),
        ),
        migrations.AddField(
            model_name='cookstage',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relates_cook_stage', to='food.food', verbose_name='Блюдо'),
        ),
    ]