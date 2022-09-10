# from django.contrib import admin

# from .models import Ingredient, Recipe, IngredientRecipe, Tag

# class IngredientRecipeLine(admin.TabularInline):
#     model = Recipe.ingredients.through
#     extra = 1

# class RecipeAdmin(admin.ModelAdmin):
#     inlines = (IngredientRecipeLine, )


# admin.site.register(Ingredient)
# admin.site.register(Recipe, RecipeAdmin)
# admin.site.register(IngredientRecipe)
# admin.site.register(Tag)

from django.contrib import admin

from .models import Ingredient, IngredientRecipe, Recipe, Tag


@admin.register(IngredientRecipe)
class IngredientAmount(admin.ModelAdmin):
    list_display = ("id", "ingredient", "recipes")
    search_fields = ("id", "ingredient", "recipes")
    list_filter = ("id", "ingredient", "recipes")
    empty_value_display = "-NONE-"


admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Tag)
