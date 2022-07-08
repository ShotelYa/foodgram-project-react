from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from recipes.views import TagViewSet, IngredientViewSet, RecipeViewSet

router = DefaultRouter()

router.register('tag', TagViewSet)
router.register('ingredient', IngredientViewSet)
router.register('recipe', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]