# Generated by Django 3.2.13 on 2022-07-24 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_recipe_ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipe_ingredient', to='recipes.Ingredient', verbose_name='Продукты'),
        ),
    ]
