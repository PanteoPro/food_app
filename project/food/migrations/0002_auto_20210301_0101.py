# Generated by Django 3.1.7 on 2021-02-28 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cook',
            name='all_calories',
            field=models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Общая каллорийность блюда'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='all_calories',
            field=models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Общая каллорийность блюда'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='total_weight',
            field=models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Вес приготовленного блюда'),
        ),
    ]
