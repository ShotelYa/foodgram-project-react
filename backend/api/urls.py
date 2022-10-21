from django.urls import include, path
from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('tag', TagViewSet)
router.register('ingredient', IngredientViewSet)
router.register('recipe', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
