from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe, Tag
from rest_framework.filters import SearchFilter
from users.models import User


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class CustomRecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(
        method='get_favorite',
        label='Favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_shopping',
        label='Is in shopping list',
    )

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'author',
            'tags',
            'is_in_shopping_cart',
        )

    def get_favorite(self, queryset, name, item_value):
        if self.request.user.is_authenticated and item_value:
            return queryset.filter(recipe_favorite__user=self.request.user)
        return queryset

    def get_shopping(self, queryset, name, item_value):
        if self.request.user.is_authenticated and item_value:
            return queryset.filter(recipe_cart__user=self.request.user)
        return queryset


# class RecipeFilter(FilterSet):
#     tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug',
#                                              to_field_name='slug',
#                                              queryset=Tag.objects.all())
#     author = filters.ModelChoiceFilter(queryset=User.objects.all())
#     is_favorited = filters.BooleanFilter(method='filter_is_favorited')
#     is_in_shopping_cart = filters.BooleanFilter(
#         method='filter_is_in_shopping_cart')

#     def filter_is_favorited(self, queryset, value):
#         if value and not self.request.user.is_anonymous:
#             return queryset.filter(favorites__user=self.request.user)
#         return queryset

#     def filter_is_in_shopping_cart(self, queryset, value):
#         if value and not self.request.user.is_anonymous:
#             return queryset.filter(cart__user=self.request.user)
#         return queryset

#     class Meta:
#         model = Recipe
#         fields = ('tags', 'author')
