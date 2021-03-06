from django.forms import ValidationError
from .models import Tag, Ingredient, Recipe, IngredientRecipe, Favorite, Cart
from rest_framework import serializers
from users.serializers import CustomUserSerializer
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth import get_user_model

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
        fields = ("id", "name", "measurement_unit")


class CartSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Cart
        fields = [
            'recipe',
            'user',
        ]

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if Cart.objects.filter(user=user, recipe__id=recipe_id).exists():
            raise ValidationError(
                'This recipe has already been added to the cart')
        return data


class ListRrecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer()
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
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Cart.objects.filter(recipe=obj, user=request.user).exists()


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'amount']


class CreateRecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    title = serializers.CharField(required=False)
    image = Base64ImageField()
    description = serializers.CharField(required=False)
    cooking_time = serializers.IntegerField()
    ingredients = AddIngredientSerializer(many=True)
    tag = serializers.PrimaryKeyRelatedField(many=True,
                                             queryset=Tag.objects.all())
    pub_date = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'image',
            'description',
            'cooking_time',
            'ingredients',
            'tag',
            'pub_date',
        ]

    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError(
                'Cooking time must be greater than 0')
        return cooking_time

    def add_ingredients_tags(self, recipe, ingredients, tags):
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient['ingredient']['id'],
                amount=ingredient['amount'])
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=self.context.get('request').user,
                                       **validated_data)
        self.add_ingredients_tags(recipe, ingredients, tags)
        return recipe

    def update(self, recipe, validated_data):
        recipe.tage.clear()
        IngredientRecipe.objects.filter(recipe=recipe).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self.add_ingredients_tags(recipe, ingredients, tags)
        return super().update(recipe, validated_data)
