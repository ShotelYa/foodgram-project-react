from django.contrib.auth import get_user_model
# from django.forms import ValidationError
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import CustomUserSerializer

from .models import Favorite, Ingredient, IngredientRecipe, Recipe, Tag

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit")

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'name', 'measurement_unit']


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Favorite.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Favorite
        fields = ['recipe', 'user']


class ListRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        ]

    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorite__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'amount']


class CreateRecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    name = serializers.CharField(required=False)
    image = Base64ImageField()
    text = serializers.CharField(required=False)
    cooking_time = serializers.IntegerField()
    ingredients = AddIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = [
            'author',
            'id',
            'image',
            'text',
            'name',
            'cooking_time',
            'ingredients',
            'tags',
        ]

    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError(
                'Cooking time must be greater than 0')
        return cooking_time

    def add_ingredients_tags(self, recipe, ingredients, tags):
        for ingredient in ingredients:
            IngredientRecipe.objects.create(recipe=recipe,
                                            ingredient=ingredient['id'],
                                            amount=ingredient['amount'])
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.add_ingredients_tags(recipe, ingredients, tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        super().update(instance, validated_data)
        instance.tags.set(tags_data)
        IngredientRecipe.objects.filter(recipe=instance).delete()
        self.add_ingredients(ingredients_data, instance)
        return instance


class RecipeSerializerShort(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
