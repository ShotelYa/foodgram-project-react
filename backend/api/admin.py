from django.contrib import admin
from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('id', 'name', 'slug')
    empty_value_display = '-NONE-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-NONE-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    list_filter = ('name', 'author')
    empty_value_display = '-NONE-'

    def count_favorite(self, obj):
        user = self.context['request'].user
        return Favorite.objects.filter(user=user, recipe=obj).count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user', )
    empty_value_display = '-NONE-'


@admin.register(Cart)
class ShopingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user', )
    empty_value_display = '-NONE-'


@admin.register(IngredientRecipe)
class IngredientAmount(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe')
    search_fields = ('id', 'ingredient', 'recipe')
    list_filter = ('id', 'ingredient', 'recipe')
    empty_value_display = '-NONE-'
