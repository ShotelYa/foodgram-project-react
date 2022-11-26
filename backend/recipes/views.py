from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from recipes.serializers import (IngredientSerializer, ListRecipeSerializer,
                                 RecipeSerializerShort, TagSerializer)
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import CustomRecipeFilter, IngredientSearchFilter
from .models import Cart, Favorite, Ingredient, IngredientRecipe, Recipe, Tag
from .pagination import CustomPagination
from .permissions import IsAuthorOrAdminOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [
        AllowAny,
    ]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [
        IsAuthorOrAdminOrReadOnly,
    ]
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('^name', )
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = ListRecipeSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly, )
    pagination_class = CustomPagination

    filter_class = CustomRecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_or_delete(self, request, model, id):
        if request.method == 'DELETE':
            obj = model.objects.filter(user=request.user, recipe__id=id)
            if obj.exists():
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'There is no such recipe'},
                            status=status.HTTP_400_BAD_REQUEST)
        if model.objects.filter(user=request.user, recipe__id=id).exists():
            return Response({'errors': 'The recipe has already been added'},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=id)
        model.objects.create(user=request.user, recipe=recipe)
        serializer = RecipeSerializerShort(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True,
            methods=('post', 'delete'),
            permission_classes=(IsAuthenticated, ))
    def shopping_cart(self, request, pk=None):
        return self.add_or_delete(request, Cart, pk)

    @action(detail=True,
            methods=('post', 'delete'),
            permission_classes=(IsAuthenticated, ))
    def favorite(self, request, pk=None):
        return self.add_or_delete(request, Favorite, pk)

    @action(
        detail=False,
        methods=('get', ),
        permission_classes=(IsAuthenticated, ),
    )
    def download_shopping_cart(self, request):
        ingredients = (IngredientRecipe.objects.filter(
            recipe__cart__user=request.user.id).values(
                'ingredient__name', 'ingredient__measurement_unit').annotate(
                    amount_sum=Sum('amount')))
        shop_list = {}
        for ingredient in ingredients:
            amount = ingredient['amount_sum']
            name = ingredient['ingredient__name']
            measurement_unit = ingredient["ingredient__measurement_unit"]
            shop_list[name] = {
                'amount': amount,
                'measurement_unit': measurement_unit
            }
            out_list = ["Ingredient list\n\n"]
        for i, value in shop_list.items():
            out_list.append(f" {i} - {value['amount']} "
                            f"{value['measurement_unit']}\n")
        return HttpResponse(
            out_list,
            {
                "Content-Type": "text/plain",
                "Content-Disposition": 'attachment; filename="out_list.txt"',
            },
        )
